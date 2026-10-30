---
name: humaniseur-fr
description: 'Use when the user supplies French text that reads like AI output and asks to naturalize it. Not for English STE rewriting: use humanizer-simple-english-asd-ste100.'
---

# Humaniseur fr

French prose that reads as machine-made carries tics a native reader spots at once: hollow verbs, stacked connectors, systematic hedging, restated sentences. This skill rewrites such text into natural French in a single pass, keeping the register the author chose and refusing to over-correct.

It is read-only. It takes French text inline or from a `.txt` or `.md` file path (read, never written) and returns rewritten French in the same turn. No file, VCS, credential, paid, published, deployed, or remote change ever results.

## Before touching a sentence

Read the source and name its register from vocabulary, morphology, and subject:

- Soutenu: formal vocabulary, subjunctive mood, complex syntax, passive constructions, literary forms.
- Courant: neutral formal standard written French, the default for professional prose and the fallback when the register cannot be determined (state the choice).
- Familier: informal vocabulary, colloquialisms, first-person constructions.

Hold the detected register from the first sentence to the last. Never upgrade or downgrade it.

Two disciplines govern the whole pass. First, one pass only: never iterate or re-apply. Second, restraint: when a pattern appears in every sentence, fix it in no more than 80 percent of them and leave at least one raw instance per pattern class per paragraph, because fixing everything reads as over-corrected. Within a single sentence, apply at most two pattern-class fixes, then stop scanning it. When a sentence already carries three flagged classes, skip further fixes there.

## The pattern catalog

Apply these per sentence, in the groups below, stopping at two fix types per sentence. Pattern numbers are stable references, not a procedure to execute in order.

### Flat AI vocabulary

1. Verbes creux. ` il s'avère que ', ` il convient de ', ` force est de constater que ', ` il importe de ', ` il appert que ', ` il va sans dire que ', ` il n'en demeure pas moins que '. Replace with a direct active verb or cut the clause entirely.
2. Substantifs en -ité abstraits. ` implémentation ', ` granularité ', ` optimalité ', ` résilience ', ` scalabilité ', ` interdépendance ', ` contextualisation ', ` performativité ', ` modularité ', ` anticipabilité '. Replace with the concrete noun or the plain verb.
3. Formules de transition vides. ` subséquemment ', ` par ailleurs ', ` dès lors ', ` en témoignent ', ` en guise de préalable ', ` à cet égard ', ` en guise de synthèse ', ` convient-il de'. Replace with ` ensuite ', ` aussi ', ` donc ', ` ainsi ', or delete the connector.
4. Adverbes en -ment hyperboliques. ` considérablement ', ` significativement ', ` amplement ', ` substantiellement ', ` on ne peut plus ', ` au plus haut point ', ` dramatiquement '. Replace with the measured adjective or cut.
5. Emprunts anglais non intégrés. ` feedback ', ` roadmap ', ` mindset ', ` onboarding ', ` livrable ', ` bottleneck ', ` framework ', ` pipeline ', ` stakeholder ', ` backend ', ` frontend ', ` fullstack ', ` rollout ', ` benchmark ', ` backlog ', ` deadline ', ` sprint ', ` agile ', ` scoper ', ` pitcher ', ` solver ', ` matcher ', ` tracker ', ` killer-feature ', ` use-case ', ` best-of-breed ', ` end-to-end '. Replace with the French term (` suivi ', ` lancement ', ` état d'esprit ', ` intégration ', ` goulot d'étranglement ', ` structure ', ` chaîne ', ` partie prenante ', ` serveur ', ` interface ', ` pile complète ', ` déploiement ', ` référence ', ` carnet de commandes ', ` délai ', ` itération ', ` souple ', ` délimiter ', ` présenter ', ` résoudre ', ` appareiller ', ` suivre ', ` caractéristique décisive ', ` cas d'usage ', ` meilleur de sa catégorie ', ` de bout en bout ').

### Connectors that force the flow

6. Listes numérotées forcées. ` Premièrement … Deuxièmement … Troisièmement … En conclusion '. Natural prose rarely uses this shape outside legal texts. Integrate the items into the sentence flow or use ` d'abord … ensuite … enfin '.
7. Connecteurs en cascade. Three or more of ` par conséquent / ainsi / dès lors / en effet / moreover ' in one paragraph. Reduce to one or two; natural French lets the logic follow from the content.
8. ` Et ce, ' et ` ce, ' comme relatives. ` Le projet, et ce, malgré les obstacles … '. Cut ` et ce ' and rewrite (` Le projet, malgré les obstacles … ').
9. ` Notamment / entre autres ' en ouverture. ` Notamment, nous observons … ', ` Entre autres, il faut … '. Replace with the plain statement (` Nous observons … ', ` Il faut … ').

### Showy repetition

10. Synonymes en cascade. ` le projet → la démarche → l'initiative → l'action ' in one paragraph. Pick one term and hold it.
11. ` Bien que / malgré le fait que ' redondants. ` Malgré le fait que ', ` Au regard du fait que '. Replace with ` bien que ', ` puisque ', ` car '.
12. ` Etc. ' en fin de phrase. Careful French prose rarely ends a list this way. Either list all items or write ` et d'autres composants '.
13. Tournures emphatiques. ` Ce qui est particulièrement digne de mention, c'est que ', ` Il convient de souligner le fait que ', ` Il est à noter que ', ` Il est un fait que '. Replace with the plain statement.
14. Hyperonymies vides. ` lesdites mesures ', ` à n'en pas douter ', ` il va sans dire ' (outside ` il va sans dire que '). Cut or replace.

### Hedging on every claim

15. Atténuations systématiques. ` dans une large mesure ', ` dans une certaine mesure ', ` dans une proportion significative ', ` il semble que ', ` il appert que ', ` il s'avère que ', ` en apparence ', ` à première vue ', ` sous certains aspects ', ` sous un certain angle ', ` force est de constater que ', ` il convient de relever '. When the statement is factually supported, make it direct. When not, write ` nous ne disposons pas de données suffisantes pour … '.
16. Modaux superlatifs. ` il est permis de croire que ', ` on serait tenté de penser que ', ` il ne serait pas exagéré de dire que ', ` il n'est pas aventureux d'affirmer que '. Remove the modal framing and state the claim directly.
17. Atténuations de conclusion. ` En définitive / en dernière analyse / en dernier recours ', ` Force est de constater que ', ` Tout compte fait ' used as openers rather than genuine summaries. Replace with a specific conclusion tied to the content.

### Sentences that restate instead of advancing

18. ` En d'autres termes / Cela étant dit / Cela étant / Ceci étant ' followed by a near-identical repetition of the previous sentence. Cut or replace with genuine new information.
19. ` Quoiqu'il en soit / Toujours est-il que ' as openers when the preceding contrast is already stated. ` mais ' or ` cependant ' suffices.
20. ` À l'instar de / De même que / À l'image de ' as filler comparatives. Keep the comparison when X is a genuine parallel; remove it when empty.

### Passive voice and heavy nominalization

21. Voix passive systématique. ` a été réalisé par ', ` a été effectuée ', ` a été mise en place ', ` a été élaboré ', ` il a été procédé à ', ` il a été décidé de ', ` il a été constaté que ', ` il a été observé que ', ` il a été établi que '. Replace with the active construction (` nous avons réalisé ', ` l'équipe a effectué ').
22. Nominalisations lourdes. ` la réalisation de ', ` la mise en œuvre de ', ` la mise en application de ', ` l'aboutissement de ', ` la procéduralisation de ', ` la contextualisation de '. Replace with the verb (` réaliser ', ` mettre en œuvre ', ` appliquer ', ` aboutir ', ` contextualiser ').
23. Pronominalisations faibles. ` se trouver être ', ` venir à ', ` en venir à ', ` il appert que ', ` il s'ensuit que '. Replace with direct verbs.
24. Doubles négations de politesse. ` il n'est pas impossible que ', ` il n'est pas inexact de ', ` il n'est pas totalement faux de ', ` il n'est pas rare que ' used to hedge. State the probability directly or replace with ` souvent ', ` parfois ', ` rarement '.

### Filler frames

25. ` Dans le cadre de / au titre de / en tant que / en qualité de ' used as empty connectors. ` Dans le cadre de nos travaux, nous avons … ' becomes ` Nous avons … '.
26. ` D'une manière générale / de façon générale / en règle générale ' as openers. Move to the end of the paragraph as a genuine summary or replace with a specific opening.
27. Phrases creuses de transition. ` Il convient de noter que ', ` Il est important de noter que ', ` Il convient de relever que ', ` Il importe de préciser que ', ` Il est loisible de penser que '. Cut or replace with the content that follows.
28. Référence à la méthode ou au processus. ` Comme nous l'avons vu / Comme évoqué précédemment / Comme indiqué ci-dessus / Tel que nous l'avons analysé ' in mid-text. Reference the specific point (` voir la section 2 ') or integrate the content directly.

### Remaining surface tics

29. Ponctuation emphatique. Triple points, stacked incise dashes, or a colon after a single short sentence. Natural French uses shorter emphatic punctuation, so reduce.
30. Formules de clôture. ` En définitive ', ` Pour tout dire ', ` En dernière analyse ', ` En dernier ressort ', ` Tout bien considéré ', ` En conclusion de quoi ' used as pure closers without new content. Integrate the conclusion into the last sentence or cut.
31. Formules protocolaires. ` Eu égard à ', ` Attendu que ', ` Vu que ', ` Dans la mesure où ' when not establishing a legal condition. Replace with ` comme ', ` puisque ', ` car '.
32. Métaphores techniques non ancrées. ` Cela ouvre la voie à ', ` Cela permet de ', ` Cela constitue un pas en avant ', ` Cela représente un enjeu majeur ', ` Cela constitue un défi de taille '. Replace with the concrete consequence.
33. Doubles comparatifs. ` plus … plus … ' or ` moins … moins … ' without proportional content. ` Plus le projet avance, plus les coûts augmentent ' is acceptable; the shape without a logical link is not.
34. Absence d'article défini. ` De manière significative ' becomes ` beaucoup ', ` peu ', or ` modérément '. ` En termes de ' is replaced by naming the domain directly.
35. Anglicismes orthographiques. ` benchmarker ', ` scoper ', ` pitcher ', ` solver ', ` tracker ', ` wrapper ', ` killer ', ` setup ', ` release ', ` build ', ` test ', ` fix ', ` patch ', ` debug ', ` feature ', ` bug ', ` hotfix ', ` release note ', ` roadmap ', ` changelog ', ` backlog ', ` sprint ', ` scrum ', ` Kanban ', ` KPI ', ` OKR ', ` SLA ', ` MVP ', ` P0 ', ` onboarding ', ` offboarding ', ` feedback ', ` feedforward ', ` mindset ', ` skillset ', ` workflow ', ` pipeline ', ` stream ', ` user story ', ` epic ', ` milestone ', ` blocker ', ` dependency ', ` integration ', ` rollout ', ` upgrade ', ` downgrade ', ` deploy ', ` ship ', ` bounce ', ` pull ', ` push ', ` fork ', ` clone ', ` merge ', ` branch ', ` commit ', ` checkout ', ` rebase ', ` squash ', ` cherry-pick ', ` tag ', ` version ', ` major ', ` minor ', ` semver ', ` breaking change ', ` issue ', ` ticket ', ` story ', ` user case ', ` use case '. Replace with the French equivalent.
36. Anglicismes syntaxiques. ` le sujet X ' for ` à propos de X '; ` avoir un impact sur ' for ` affecter '; ` avoir lieu ' for ` se dérouler '; ` être en ligne avec ' for ` correspondre à '; ` en temps réel ' for ` instantanément '.
37. ` À noter ' en début de paragraphe. ` À noter que ', ` Il est à noter que '. ` À noter : ' is acceptable as a marginal annotation, never as a paragraph opener.
38. Listes hybrides. Mixing numbered and bulleted lists in one list. Use one consistent format.

## When the input cannot be handled

- No text supplied and no file readable: return ` Veuillez fournir du texte français à naturaliser.'
- Source text is not French (over half the tokens are non-French): return ` Ce texte n'est pas en français. Cette compétence s'applique uniquement au français.'
- The file path points to a non-text file: return ` Le fichier n'est pas lisible comme texte.'
- A sentence already carries three flagged classes: skip further fixes there and add nothing more.
- A pattern appears in every sentence: leave at least one raw instance and never fix all of them.

Long texts are processed one paragraph at a time. When interrupted, return the paragraphs already processed and state: ` Naturalisation partielle : N paragraphes sur M traités.'

## What you hand back

The rewritten French text in the preserved register, with no more than two pattern-class fixes per sentence and no pattern fixed in more than 80 percent of its instances across the whole text.
