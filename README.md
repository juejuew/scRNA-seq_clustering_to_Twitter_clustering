# Application of Single-cell RNA-seq Data Clustering to Twitter Data

Traditional topic modeling schemes including Latent Dirichlet allocation (LDA) and Latent Semantic Analysis (LSA) have been widely adopted in the social sciences, but typically struggle to cope well with short texts. We observe that microblog data such as Twitter data, once formatted as a word-document matrix, share important properties with single-cell RNA sequencing (scRNA-seq) data; in particular, both types of data are high-dimensional, consist of small integer counts, and have sparse non-zero entries. Advanced clustering methods have been designed for scRNA-seq data to identify cell types, so we translate scRNA-seq clustering methods to cluster Twitter data.

## Preprocessing 
* In the folder `P1_preprocessing` *
The first step is to preprocess the tweets from four distinct users (`four_users.csv`) and the "jobs" tweets (`jobs_tweets_sampled_three_month.csv`). The code for preprocessing can be found in `preprocessing.ipynb`.
