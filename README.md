# Downloader for object resources and images on museum-digital

## Purpose

This script serves to back up all images and resources for a given museum from museum-digital.

## Setup

This script works best with an own, dedicated user account. In this section, the creation of a new user account with the necessary permissions (and only those), the creation of an authentication token and the setup for this script will be explained.

### Creating an own user for backups

Create a new user account. Select "specifically determined" as the user role. 

![Creating a new user (role: _specifically determined_)][img_user_1_new_user]

This user role sets all permissions to "disabled" by default. As this user only needs access to images / resources and should never have access to anything else, allowing viewing resources.

![Set the permission for resources of objects to _viewing_.][img_user_2_permissions]

This script logs in using authentication tokens. Generate one for the user. Click on user in the navigation to access the list of users. Then click on "Auth Token" in the rightmost column. Click confirm, and copy the generated token to some safe place.

![Click on Auth Token in the last column.][img_user_3_generate_token]
![Copy the token.][img_user_4_copy_token]

[img_user_1_new_user]: screenshots/screenshot-user_1_new.png "Creating a new user (role: _specifically determined_)"

[img_user_2_permissions]: screenshots/screenshot-user_2_permissions.png "Set the permission for resources of objects to _viewing_."

[img_user_3_generate_token]: screenshots/screenshot-user_3_generate_token.png "Click on Auth Token in the last column."

[img_user_4_copy_token]: screenshots/screenshot-user_4_copy_token.png "Copy the token."

### Write the settings file

Copy or rename the sample for the settings file to `settings.xml`. It must remain located in the same folder as the program. Then, open the settings file and insert the auth token you generated in the previous step and the correct URL for your museum. A correct settings.xml may look as follows:

```
<xml>
  <authtoken>1eee9fe290359a34f224712debed9d83898b5436cebf3cfcc0cf4266a97b</authtoken>
  <url>https://www.museum-digital.de/sandkasten/musdb/lists.php?musid=1</url>
</xml>
```

### Running the script

To run the script, double-click on it. It will fetch an index of all the available resources including the last time they were updated. This index is then compared to a local index of already downloaded files so that files will not be downloaded twice. If the file was not included in the local index, it is downloaded and marked as such in the local index. All downloaded files will be located in a subdirectory (`files`) of the directory the script is located in.

Note that the script waits 3 seconds after downloading a file, to reduce server load.

