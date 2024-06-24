# Recipe Book Project

Welcome to my Recipe Book Website, where you can Register, Enter Recipes, Sort for them, And change them is you made a mistake.
***
## Features 

Index Page - Where you Can Choose to Register a New Account Or Login with an Existing one

![צילום מסך 2024-06-23 232217](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/ea53a270-4cd0-411a-b2e8-0a380a509cfe)
***
Register Page - 

![צילום מסך 2024-06-23 232247](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/ab2f9c62-ebde-40da-ae11-d163e7d6720d)
***
Login Page -



![צילום מסך 2024-06-23 233410](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/ead4c58c-723e-4d37-b720-822656311cbe)
***
Dashboard Page - 
- Where you can Choose to Enter a New Recipe
- See all The Existing Recipes in the Recipe Book
- Logout if you Want to Exit the Current Session

![צילום מסך 2024-06-23 232309](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/f9923971-2bd7-426e-8bca-b5490b514087)
***
Recipe Entering Page - Where you can Enter 
- Recipe Name
- Recipe Time
- Recipe Description
- Difficulty
- Ingredients

  ![צילום מסך 2024-06-23 234126](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/e160f631-b666-4281-9cc8-9213f294b218)
  ***
Recipe Book page - Where you can Sort For these Categories
- Time
- Difficulty
  
![צילום מסך 2024-06-23 232357](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/dadde46e-1f51-4070-bc7e-9f2a34377509)
***
Sorting By Time - 

![צילום מסך 2024-06-23 232407](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/b99ac7dc-b823-43f5-ba9d-39de954d832e)
***
Sorting By Difficulty - 

![צילום מסך 2024-06-23 235009](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/9921b944-f8a7-4abd-977d-599637cda57b)
***
A Recipe Page - Where you Can Edit the Recipe

![צילום מסך 2024-06-23 232438](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/97478b7d-9a53-43f3-82fe-6459f9d52525)
***
Edit Recipe Page - Where you Have all the values inside the Boxes and you can Alter Them

![צילום מסך 2024-06-23 232449](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/b0ed848e-fff5-491b-b4e9-6b8712049fb1)
***
# Tools 
In My Project I use Modern Technologies and Tools to improve and Optimize the Development, Testing and Deployment Process. In the Project I use these tools especially in the various Devops Processes.

## Continuous Integration and Delivery

- jenkins : An open-source automation server that enables developers around the world to reliably build, test, and deploy their software. Jenkins orchestrates our CI/CD pipeline, integrating seamlessly with GitHab for a smooth development
process. in this project used with multibranch pipeline t orun diffrent workflows.

![jenkins](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/99f640be-0b0d-4aa1-ad51-2fd2cb87c222)

## Containerization and Artifact Storage

- Docker : Dockerize our application and storing the image, in Dockerhub. allows us to run and deploy the application without conditions and limitations.

![docker](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/27622feb-a28f-4273-987f-08c8358d082f)

## Deployment

- Argocd : Argo CD is an open-source tool used for managing and automating the operation of applications in Kubernetes. It focuses on easily and safely managing and deploying applications in a Kubernetes environment.. When using Argo CD, you define applications through relatively simple and readable YAML. The application definition includes all the necessary information to specify the import and deployment of the application in your Kubernetes environment.

![argocd](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/cab5e27f-7e8e-4159-8c1b-04540d7b9d0f)

## Kubernetes

- Kind (Kubernetes In Docker): Kind is a tool for creating local Kubernetes clusters using Docker containers as nodes. It simplifies testing and development by allowing multi-node Kubernetes setups on a single machine, leveraging Docker for efficient cluster management and integration with Kubernetes features. This enables faster application development and testing without complex infrastructure setup.

![kubernetes](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/d015ddea-6ff0-4ce9-a81f-1c3af642a0b0)

## Monitoring 

- grafana :Grafana is an open-source analytics and monitoring platform that allows you to query, visualize, alert on, and understand metrics no matter where they are stored. It provides a powerful and flexible platform for creating, exploring, and sharing dashboards and data visualizations.

![grafana](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/dc01ad25-54fa-4af3-b034-3add1939e903)

- prometheus : Prometheus is designed for monitoring the performance and availability of applications and infrastructure. It collects metrics from configured targets at regular intervals, evaluates rule expressions, displays the results, and can trigger alerts if certain conditions are met.

![prometheus](https://github.com/Ilaysb1/Recipe-Book/assets/144901363/6133432b-fb0a-4211-95fb-34a0acfd4292)

***
# Run localy

## Clone
```
git clone https://github.com/Ilaysb1/Recipe-Book.git
```
## Docker compose file :

```
version: '3'

services:
  flask_app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongo
    environment:
      MONGO_URI: mongodb+srv://ilaysb:Ilaysb12@cluster0.f1l3dro.mongodb.net/testDB  
    volumes:
      - ./main.py:/app/main.py 
      - ./static:/app/static   
      
  mongo:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
  
  test:
    build: 
      context: .
      dockerfile: Dockerfile.test
    environment:
      MONGO_URI: mongodb+srv://ilaysb:Ilaysb12@cluster0.f1l3dro.mongodb.net/testDB  
    depends_on:
      - mongo
      - flask_app

volumes:
  mongodb_data:
```

## Start the Application
```
 docker-compose up -d
```

