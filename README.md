# Application of Single-cell RNA-seq Data Clustering to Twitter Data
**Docker image:** https://hub.docker.com/r/juejue64807761/scrnaseq_twicluster

Traditional topic modeling schemes including Latent Dirichlet allocation (LDA) and Latent Semantic Analysis (LSA) have been widely adopted in the social sciences, but typically struggle to cope well with short texts. We observe that microblog data such as Twitter data, once formatted as a word-document matrix, share important properties with single-cell RNA sequencing (scRNA-seq) data; in particular, both types of data are high-dimensional, consist of small integer counts, and have sparse non-zero entries. Advanced clustering methods have been designed for scRNA-seq data to identify cell types, so we translate scRNA-seq clustering methods to cluster Twitter data.

## Preprocessing 
##### In the folder `P1_preprocessing`
* The first step is to preprocess the tweets from four distinct users (`four_users.csv`) and the "jobs" tweets (`jobs_tweets_sampled_three_month.csv`). The code for preprocessing can be found in `preprocessing.ipynb`. 

* After preprocessing, you will obtain the term-document matrix and the document information data for the "four-user" tweets and "jobs" tweets respectively. They are the inputs for the other two parts. 

* Specifically,
  - **Term-document Matrix**: rows are terms, columns are tweets, and entries are corresponding word frequency
  - **document information data**: a data frame where the rows are tweets and columns are tweets' features

## Prelimilary analysis on the four-user tweets
##### In the folder `P2_scRNAseq_LDA_NMF`
* In the second step, on the four-user tweets, we compare the performance of two scRNAseq clustering toolkits (Monocle3 and Seurat) with two traditional topic modeling methods (LDA and NMF). 

* The implementation of LDA and NMF is in `LDA_NMF/LDA_and_NMF_evaluation_metrics.ipynb`. Then, you can calculate the summary tables by using `LDA_NMF/LDA_NMF_summary_table.ipynb`

* To implement Monocle3/Seurat in this analysis, first run `M3_tfidf.ipynb`/`S_tfidf.ipynb` to scale the term-documanr matrix. Then, run `Monocle3.ipynb`/`Seurat.ipynb` to implement it and find topic clusters. Next, calculate the evaluation metrics using `M3_evaluation_metrics.ipynb`/`S_evaluation_metrics.ipynb`

* Finally, use `four_Evaluation_visualization.ipynb` and `jobs_Evaluation_visualization.ipynb` to visualize the evaluation results. 

## Implement and evaluate the proposed workflow
##### In the folder `P3_Proposed_workflow`
* In the third step, we implement the proposed workflow that is based on Monocle3. Before the implementation and the evaluation, use `HCCA_jobs.ipynb` to obtain the labels from the hand-created classification algorithm. We use these labels as the ground truth for the topics of "jobs" tweets. Moreover, you can use `HCCA_validation_jobs.ipynb` -> `validation_of_HCCA.ipynb` to validate the hand-created classification algorithm. 

* Next, implement the proposed workflow on the four-user tweets and "jobs" tweets using `four_proposed_Workflow.ipynb` and `jobs_proposed_Workflow.ipynb` respectively. During the implementation, use `HDBSCAN_or_DBSCAN.ipynb` to separate tiny clusters with main clusters; use `PW_tfidf.ipynb` to scale the term-document matrix. 

* Finally, use `PW_evaluation_metrics.ipynb` to calculate the evaluation metrics. Visualization of the evaluation can be found in `P2_scRNAseq_LDA_NMF/four_Evaluation_visualization.ipynb` and `P2_scRNAseq_LDA_NMF/jobs_Evaluation_visualization.ipynb`

## Related links

Monocle3: https://cole-trapnell-lab.github.io/monocle3/docs/clustering/

Seurat: https://satijalab.org/seurat/v3.1/pbmc3k_tutorial.html

## Reference 
Ferg, Robyn. Modern Survey Estimation with Social Media and Auxiliary Data. Diss. 2020.

Conrad, Frederick G., et al. "Social media as an alternative to surveys of opinions about the economy." Social Science Computer Review 39.4 (2021): 489-508.

Levine, Jacob H., et al. "Data-driven phenotypic dissection of AML reveals progenitor-like cells that correlate with prognosis." Cell 162.1 (2015): 184-197.

Blei, David M., Andrew Y. Ng, and Michael I. Jordan. "Latent dirichlet allocation." Journal of machine Learning research 3.Jan (2003): 993-1022.

Lee, Daniel D., and H. Sebastian Seung. "Learning the parts of objects by non-negative matrix factorization." Nature 401.6755 (1999): 788-791.




