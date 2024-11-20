# fb-movies-app
Survey platform to study and analyze in-group algorithmic bias in social networking platforms

### Frameworks used:

* Angular for UI 

* Django for APIs

### Current Service Information

- The working App:
    - http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/
    - Django admin (http://44.204.168.187/admin/)
    - Backend: current running on movies-backend-v2 ([http://44.204.168.187](http://44.204.168.187/admin/))
    - S3: **fb-movies-ui-test**
- Frontend is built with Angular
    - My current working versions
        - Angular CLI: 10.0.8
        - Node: 12.11.1
        - OS: darwin x64
        - Angular: 10.0.14
- Backend is built with Django
    - Python 3.8.10 Environment creation with python’s virtual env
- Web Server: Apache ( `/etc/apache2/sites-available/` )
- Infra:
    - AWS EC2
        - t3.large
        - AMI: `ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20211021`
    - S3 with static website enabled

### Database Tables: 
* Fnames (Input List of first names)

* Lnames (Input List of last names)

* Movies (Input List of movies)

* Users (Output List of all users with User ID who use the portal with specific details)

* Output (Output generated out of User Experience tracked with User ID)

* Dynamics (Updatable content for specific pages)

* UserPatterns

### Setup instructions can be found inside the UI/Backend folders

### Why to do when the IP of the EC2 Instance change?

- Since there's no CI/CD or other DevOps tool set up, When the EC2 instance’s IP address changed, we need to manually update it to both frontend and backend code.
- Frontend:
    - Update the new IP address in `global-constants.ts`
    - Rebuild the site `ng build --prod` . (The developer needs to set up the npm environment prior to the build)
    - Upload to S3 Bucket manually with the configuration.
        - Add the Bucket Policy like this

        ```bash
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPermission",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::fb-movies-ui-test/*"
                }
            ]
        }
        ```

        - Enable static website hosting
- Backend:
    - Add the new IP to `ALLOWED_HOSTS` in django’s `setting.py`
    - Add the S3 bucket URL to `CORS_ALLOWED_ORIGINS` in django’s `setting.py`
    - `sudo service apache2 restart` to restart the server
