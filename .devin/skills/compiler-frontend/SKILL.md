---
name: compiler-frontend
description: 'Use when building a lexer, Pratt or recursive-descent parser, AST, symbol table, type checker, or LLVM IR emitter for a language or DSL. Not for optimizing IR.'
---

# Compiler frontend

This skill builds the front half of a language or DSL: lexer, expression and statement parsers, symbol table, type checker, and LLVM IR emitter. It starts from a language description (the token set, the grammar or example programs, the operators with precedence and associativity), works in C or Rust (C samples below use the LLVM C API in `llvm-c/`; in Rust use the `inkwell` or `llvm-sys` crates), covers only the requested stages (any subset of lexer, parser, symbol table, type checker, IR emitter), and tests against at least one valid program per stage plus one program with an error the stage must report.

Writes stay inside the frontend source files named for the task; rollback is version control. Nothing touches a remote resource. Each delivered stage compiles, runs on the supplied test inputs, and passes its verification: token streams match, precedence tests pass, undefined and mismatched types are reported, generated IR passes the LLVM verifier. When a stage cannot finish, the report states which stages passed and which are blocked instead of claiming partial work as complete.

## Fix the pipeline first

The pipeline is source to lexer (tokens) to parser (AST) to type checker to IR generator to LLVM IR. Write down which stages this task delivers and each stage's input and output types before writing code.

## Lex with a hand-written state machine

Tokens carry a kind, a pointer into the source, a length, and any literal value. Skip whitespace, then dispatch on the first character: digits build an integer, letters build an identifier, single characters map to punctuation.

```c
typedef enum { TOK_EOF, TOK_INT, TOK_IDENT, TOK_PLUS, TOK_MINUS,
               TOK_LPAREN, TOK_RPAREN, TOK_SEMI, TOK_EQ, TOK_RETURN } TokenKind;

typedef struct { TokenKind kind; const char *start; int length; int64_t int_val; } Token;
typedef struct { const char *src; int pos; int line; } Lexer;

Token lexer_next(Lexer *l) {
    while (l->src[l->pos] == ' ' || l->src[l->pos] == '\n') l->pos++;
    const char *start = &l->src[l->pos];
    if (isdigit((unsigned char)l->src[l->pos])) {
        int64_t val = 0;
        while (isdigit((unsigned char)l->src[l->pos]))
            val = val * 10 + (l->src[l->pos++] - '0');
        return (Token){ TOK_INT, start, (int)(&l->src[l->pos] - start), val };
    }
    if (isalpha((unsigned char)l->src[l->pos])) {
        while (isalnum((unsigned char)l->src[l->pos])) l->pos++;
        return (Token){ TOK_IDENT, start, (int)(&l->src[l->pos] - start), 0 };
    }
    switch (l->src[l->pos++]) {
        case '+': return (Token){ TOK_PLUS, start, 1, 0 };
        case '(': return (Token){ TOK_LPAREN, start, 1, 0 };
        case ')': return (Token){ TOK_RPAREN, start, 1, 0 };
        case ';': return (Token){ TOK_SEMI, start, 1, 0 };
        default:  return (Token){ TOK_EOF, start, 0, 0 };
    }
}
```

A generated lexer is the alternative when the token set is large: `flex lexer.l && gcc -o lexer lex.yy.c -lfl`. With flex, order rules so the longest match wins and keywords precede the identifier rule; on a token clash, rely on longest match and move keyword rules before the identifier rule. Every test input must produce the expected token stream, including the EOF token.

## Parse expressions with Pratt, statements by recursion

Each infix operator has a left and a right binding power; a higher power binds tighter, and right associativity is a right power one below the left. The loop consumes operators while their left power is at least the minimum.

```c
typedef enum { AST_INT, AST_BINOP, AST_VAR } AstKind;
typedef struct AstNode {
    AstKind kind;
    union {
        int64_t int_val;
        struct { int op; struct AstNode *lhs, *rhs; } binop;
        char *name;
    };
} AstNode;

enum { BP_NONE = 0, BP_SUM = 10, BP_PRODUCT = 20 };

AstNode *parse_expression(Parser *p, int min_bp) {
    AstNode *left = parse_prefix(p);
    for (;;) {
        int lbp, rbp;
        if (!infix_binding_power(p->cur.kind, &lbp, &rbp) || lbp < min_bp) break;
        int op = p->cur.kind;
        advance(p);
        AstNode *right = parse_expression(p, rbp);
        left = make_binop(op, left, right);
    }
    return left;
}
```

Capture the operator before `advance`: reading `p->cur.kind` after the recursive call returns the wrong token. When precedence comes out wrong, the binding-power table is wrong; fix the table and re-run the expression table test, covering mixed precedence and associativity.

Parse statements with recursive descent, one function per nonterminal:

```c
AstNode *parse_statement(Parser *p) {
    if (p->cur.kind == TOK_IDENT && peek(p) == TOK_EQ) {
        char *name = take_ident(p);
        advance(p);
        AstNode *expr = parse_expression(p, BP_NONE);
        expect(p, TOK_SEMI);
        return make_assign(name, expr);
    }
    if (match(p, TOK_RETURN)) {
        AstNode *expr = parse_expression(p, BP_NONE);
        expect(p, TOK_SEMI);
        return make_return(expr);
    }
    return parse_expression_statement(p);
}
```

Every branch must consume at least one token or return; a branch that neither advances nor returns is how the parser loops forever. Audit every branch of the failing nonterminal for `advance` or `return` and add the missing progress. Every statement form in the test inputs must parse.

## Scope names with a chain of scopes

Lookup walks from the innermost scope to the root; definition writes only into the current scope, so shadowing an outer name is allowed and redefining a name in the same scope is an error.

```c
typedef struct Symbol { char *name; Type *type; LLVMValueRef llvm_val; struct Symbol *next; } Symbol;
typedef struct Scope { Symbol *symbols; struct Scope *parent; } Scope;

Symbol *scope_lookup(Scope *s, const char *name) {
    for (Scope *cur = s; cur; cur = cur->parent)
        for (Symbol *sym = cur->symbols; sym; sym = sym->next)
            if (strcmp(sym->name, name) == 0) return sym;
    return NULL;
}

void scope_define(Scope *s, const char *name, Type *type) {
    Symbol *sym = malloc(sizeof *sym);
    if (!sym) abort();
    sym->name = strdup(name); sym->type = type; sym->llvm_val = NULL;
    sym->next = s->symbols; s->symbols = sym;
}
```

When a duplicate is accepted or shadowing is rejected, lookup and define are using the wrong scope: lookup walks parents, define writes the current scope only. Replace the linked list with a hash map when scopes hold more than a few dozen names. Shadowing must resolve to the inner name and a same-scope duplicate must be rejected.

## Check types by walking the AST

Integers have the integer type; a variable takes its symbol's type or reports "undefined"; a binary operation requires equal operand types.

```c
Type *check_expr(Scope *s, AstNode *node) {
    switch (node->kind) {
    case AST_INT: return type_int();
    case AST_VAR: {
        Symbol *sym = scope_lookup(s, node->name);
        if (!sym) error("undefined variable %s", node->name);
        return sym->type;
    }
    case AST_BINOP: {
        Type *lt = check_expr(s, node->binop.lhs);
        Type *rt = check_expr(s, node->binop.rhs);
        if (!type_equal(lt, rt)) error("type mismatch in binary op");
        return lt;
    }
    }
    return type_void();
}
```

For an ML-style language with inference, assign a type variable to each unknown and unify on constraints (Hindley-Milner); that is a separate stage, not a change to the checker above. Each error test input must produce its expected diagnostic and valid inputs must pass.

## Recover from syntax errors in panic mode

On error, advance until a synchronizing token, then resume. Pick the synchronizing set per nonterminal (statement end `;`, block end `}`, statement-start keywords).

```c
void synchronize(Parser *p) {
    advance(p);
    while (p->cur.kind != TOK_EOF) {
        if (p->prev.kind == TOK_SEMI) return;
        if (p->cur.kind == TOK_RETURN || p->cur.kind == TOK_IDENT) return;
        advance(p);
    }
}
```

Without synchronization, one mistake cascades into many; an input with two independent errors must report both. Error productions for common mistakes and single-token insertion or deletion are the next steps when the frontend serves an editor.

## Emit LLVM IR through the C API and verify it

Create types from a context, build instructions through a builder, and use the typed load: the untyped `LLVMBuildLoad` is gone from the current C API (LLVM 23.1.4) and `LLVMInt32Type()` without a context is deprecated.

```c
#include <llvm-c/Core.h>
#include <llvm-c/Analysis.h>

LLVMContextRef ctx; LLVMModuleRef module; LLVMBuilderRef builder;

LLVMValueRef codegen_expr(Scope *s, AstNode *node) {
    switch (node->kind) {
    case AST_INT:
        return LLVMConstInt(LLVMInt32TypeInContext(ctx), (unsigned long long)node->int_val, 1);
    case AST_BINOP: {
        LLVMValueRef l = codegen_expr(s, node->binop.lhs);
        LLVMValueRef r = codegen_expr(s, node->binop.rhs);
        if (node->binop.op == TOK_PLUS) return LLVMBuildAdd(builder, l, r, "add");
        break;
    }
    case AST_VAR: {
        Symbol *sym = scope_lookup(s, node->name);
        return LLVMBuildLoad2(builder, LLVMInt32TypeInContext(ctx), sym->llvm_val, node->name);
    }
    }
    return NULL;
}
```

After emitting, dump and verify: `LLVMDumpModule(module);` and `LLVMVerifyModule(module, LLVMReturnStatusAction, &err);` where `LLVMVerifyModule` is declared in `llvm-c/Analysis.h`. A verifier failure is an IR type mismatch, usually signedness, pointer level, or a load with the wrong type argument; read the verifier message and fix the emitter for that node kind. The verifier must return success on every valid test input.

Hand back a delivery listing each source file created or edited per stage, the per-stage verification (test inputs run with the observed token stream, tree, diagnostic, or verifier result), and any open decisions: grammar ambiguities or type rules the language description left undefined, with the choice made.
