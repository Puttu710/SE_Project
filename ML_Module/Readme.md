### Architecture used:
![The Architecture](https://github.com/BhaviD/SE_Project/blob/ML/arch_design/ML_Module.jpg)

### Evaluation of the tag predictor model:
![](https://github.com/BhaviD/SE_Project/blob/ML/ML_Module/evaluation.png)


### Instructions:
1. To get similar questions to your given question Q:
  * call <code> searchresults(Q, no_of_questions) </code> in *search.py* file
    * The output will be a json consisting of <code> {title, url, tags, votes, body} </code> 
2. To get predicted tags for any question Q:
  * call <code> predict_tags(Q) in *search.py* file
    * The output will be a list of predicted tags
