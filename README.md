# CalmCube
The ^^ indicates the end of the command, don't include ^^ in the command.

https://www.raspberrypi.org/documentation/linux/usage/commands.md
^^ great resource for linux (raspberry pi terminal) commands


Some note worthy commands (add more useful ones if you wish):

ls
^^lists directories (folder/files) currently within the your current directory

cd NEW_DIRECTORY
^^used to change directory to a directory lower then the one currently in

cd ..
^^goes back a directory (goes up one level)

git clone -b BRANCH_NAME REPOSITORY_URL
^^the above is downloads a single branch

git clone -b BRANCH_NAME REPOSITORY_URL NAME_DIRECTORY_SAVED_AS
^^this is the same as the previous command but the file gets saved as a different directory name so it doesn't conflict with the old save

rm -r DIRECTORY_NAME
^^removes the whole directory, careful cuz it's permanent, you have to remove/rename the old clone to be able to download a new one

