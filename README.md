# House_Price_Prediction_GL

## Explanation of the Model built

All python scripts use the configuration.txt file 

1.  directory -->> load_csv_to_mongo

     Standalone, independent code to upload the train and test csv files to MongoDB hosted on an AWS machine.

2.  Created a base Pyspark image with all the required dependencies.

    DOCKER BASE IMAGE: gaddamsrikanth24/pyspark-models:latest

3.  Created a docker volume - "house_prices" and using "/usr/src/app/" as the destination directory for persisiting all the data.


4. Fetch data from MongoDB and write to a csv file on docker volume

   Python Code: load_csv_mongodb.py
   
   Dockerfile: fetchDataFromDB.dockerfile
   
   DockerImage: gaddamsrikanth24/pyspark-models:fetch_data

5. Create a pipeline with all data preprocessing transformations in place and export a pipeline.

   Python Code: data_preprocess_pipeline.py
   
   Dockerfile: preprocess_pipeline.dockerfile
   
   DockerImage: gaddamsrikanth24/pyspark-models:preprocess
   

6. Load pipeline from last step, apply it on data fetched from DB.

   Python Code: data_preprocess.py
   
   Dockerfile: data_preprocess.dockerfile
   
   DockerImage: gaddamsrikanth24/pyspark-models:data_preprocess
   

7. Create a feature process pipeline fitted on preprocessed data, and export.

   Python Code: feature_processing_pipeline.py
   
   Dockerfile: feature_processing.dockerfile
   
   DockerImage: gaddamsrikanth24/pyspark-models:feature_processing
   

8. Load feature modelling and scaling pipeline from last step, apply it on preprocessed data.

    * Here, we are also using GBTRegressor model with hyper-parameters to generate a predicted data CSV file.
    
   Python Code: feature_process.py
   
   Dockerfile: feature_model.dockerfile
   
   DockerImage: gaddamsrikanth24/pyspark-models:feature_model
   
   
9. Evaluate metrics from the CSV file generated in the previous step.

   Python Code: evalMetrics.py
   
   Dockerfile: eval.dockerfile
   
   DockerImage: gaddamsrikanth24/pyspark-models:eval_metrics  
  
