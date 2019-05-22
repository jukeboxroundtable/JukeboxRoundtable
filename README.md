[![Build Status](https://travis-ci.com/jukeboxroundtable/JukeboxRoundtable.svg?branch=master)](https://travis-ci.com/jukeboxroundtable/JukeboxRoundtable)
# Jukebox Roundtable

# Development Setup
* Clone our repository locally.
* Get the Firebase database set up:
  * Create a directory called 'instance' in the top level of the project. (This will keep git from tracking it)
  * Accept an invitation of ownership from the JukeboxRT firebase project.
  * Create a service key:
    * In firebase, go to `project settings`.
    * Click on `service accounts`.
    * Click on `generate new private key`.
    * Save this file in the 'instance' directory you created.
  * Set up Environment Variables:
    * The file you saved in your 'instance' directory will have almost all of the environment variables you will need.
    * List of environment variables needed:
      * FIREBASE_TYPE
      * FIREBASE_PROJECT_ID
      * FIREBASE_PRIVATE_KEY_ID
      * FIREBASE_PRIVATE_KEY
      * FIREBASE_CLIENT_EMAIL
      * FIREBASE_CLIENT_ID
      * FIREBASE_AUTH_URI
      * FIREBASE_TOKEN_URI
      * FIREBASE_DATABASE
        * This one can be found on Firebase (ex. FIREBASE_DATABASE=https://jukeboxrt-10000.firebaseio.com/)
