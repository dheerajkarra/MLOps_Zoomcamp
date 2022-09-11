# Model development 

In this section, the model is developed for top n independent variables from the dataset using SelectKBest class of sklearn. "chi2" method is used as scoring function. 

Linear regression is used to predict energy usage. I have saved the DictVectorizer and linear regression model as lin_reg.bin, which will be used as input model in other sections.

### Steps to run the script

1. Run the script modelling.py. It will generate lin_reg.bin file, which will be used in other sections.