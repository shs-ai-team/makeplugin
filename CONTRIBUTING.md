# How to contribute to the project

## General setup

We use an organization based approach. Everone of our team is using the same repo as a clone. We do not fork it. Our main branch is protected and merging into it needs approval from at least one other team member. This means, we clone the repo and then check out our feature-branch to work in it. Of course this means we also have to fetch and synch the main branch regularly to have the newest state of the main branch before pushing a PR

## API Key handling with .env files

Every team member has his or her own AI/ML API key. This key is used inside the /backend folder to be used when developing or testing the solution. The /backend implementation contains a .gitignore file that excludes the .env file in this folder from being published to the repo. This prevents leaking of the secrets contained in the .env file. Make sure to place your API key and all the other secrets you need to develop your part of the solution ONLY in this .env file in the /backend folder. Of course you also can use environment variables which you export per session instead of an .env file. Making sure to follow this guideline keeps our developer experience and our project more fun and healthy. The same goes for the /frontend folder. Only use .env files in the /frontend folder for storing secrets if you have the need for them. The .gitignore file there is taking care of excluding your .env file with your secrets.
