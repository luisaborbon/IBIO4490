

# Introduction to Linux

## Preparation

1. Boot from a usb stick (or live cd), we suggest to use  [Ubuntu gnome](http://ubuntugnome.org/) distribution, or another ubuntu derivative.

2. (Optional) Configure keyboard layout and software repository
   Go to the the *Activities* menu (top left corner, or *start* key):
      -  Go to settings, then keyboard. Set the layout for latin america
      -  Go to software and updates, and select the server for Colombia
3. (Optional) Instead of booting from a live Cd. Create a partition in your pc's hard drive and install the linux distribution of your choice, the installed Os should perform better than the live cd.

## Introduction to Linux

1. Linux Distributions

   Linux is free software, it allows to do all sort of things with it. The main component in linux is the kernel, which is the part of the operating system that interfaces with the hardware. Applications run on top of it. 
   Distributions pack together the kernel with several applications in order to provide a complete operating system. There are hundreds of linux distributions available. In
   this lab we will be using Ubuntu as it is one of the largest, better supported, and user friendly distributions.


2. The graphical interface

   Most linux distributions include a graphical interface. There are several of these available for any taste.
   (http://www.howtogeek.com/163154/linux-users-have-a-choice-8-linux-desktop-environments/).
   Most activities can be accomplished from the interface, but the terminal is where the real power lies.

### Playing around with the file system and the terminal
The file system through the terminal
   Like any other component of the Os, the file system can be accessed from the command line. Here are some basic commands to navigate through the file system

   -  ``ls``: List contents of current directory
   - ``pwd``: Get the path  of current directory
   - ``cd``: Change Directory
   - ``cat``: Print contents of a file (also useful to concatenate files)
   - ``mv``: Move a file
   - ``cp``: Copy a file
   - ``rm``: Remove a file
   - ``touch``: Create a file, or update its timestamp
   - ``echo``: Print something to standard output
   - ``nano``: Handy command line file editor
   - ``find``: Find files and perform actions on it
   - ``which``: Find the location of a binary
   - ``wget``: Download a resource (identified by its url) from internet 

Some special directories are:
   - ``.`` (dot) : The current directory
   -  ``..`` (two dots) : The parent of the current directory
   -  ``/`` (slash): The root of the file system
   -  ``~`` (tilde) :  Home directory
      
Using these commands, take some time to explore the ubuntu filesystem, get to know the location of your user directory, and its default contents. 
   
To get more information about a command call it with the ``--help`` flag, or call ``man <command>`` for a more detailed description of it, for example ``man find`` or just search in google.


## Input/Output Redirections
Programs can work together in the linux environment, we just have to properly 'link' their outputs and their expected inputs. Here are some simple examples:

1. Find the ```passwd```file, and redirect its contents error log to the 'Black Hole'
   >  ``find / -name passwd  2> /dev/null``

   The `` 2>`` operator redirects the error output to ``/dev/null``. This is a special file that acts as a sink, anything sent to it will disappear. Other useful I/O redirection operations are
      -  `` > `` : Redirect standard output to a file
      -  `` | `` : Redirect standard output to standard input of another program
      -  `` 2> ``: Redirect error output to a file
      -  `` < `` : Send contents of a file to standard input
      -  `` 2>&1``: Send error output to the same place as standard output

2. To modify the content display of a file we can use the following command. It sends the content of the file to the ``tr`` command, which can be configured to format columns to tabs.

   ```bash
   cat milonga.txt | tr '\n' ' '
   ```
   
## SSH - Server Connection

1. The ssh command lets us connect to a remote machine identified by SERVER (either a name that can be resolved by the DNS, or an ip address), as the user USER (**vision** in our case). The second command allows us to copy files between systems (you will get the actual login information in class).

   ```bash
   
   #connect
   ssh USER@SERVER
   ```

2. The scp command allows us to copy files form a remote server identified by SERVER (either a name that can be resolved by the DNS, or an ip address), as the user USER. Following the SERVER information, we add ':' and write the full path of the file we want to copy, finally we add the local path where the file will be copied (remember '.' is the current directory). If we want to copy a directory we add the -r option. for example:

   ```bash
   #copy 
   scp USER@SERVER:~/data/sipi_images .
   
   scp -r USER@SERVER:/data/sipi_images .
   ```
   
   Notice how the first command will fail without the -r option

See [here](ssh.md) for different types of SSH connection with respect to your OS.

## File Ownership and permissions   

   Use ``ls -l`` to see a detailed list of files, this includes permissions and ownership
   Permissions are displayed as 9 letters, for example the following line means that the directory (we know it is a directory because of the first *d*) *images*
   belongs to user *vision* and group *vision*. Its owner can read (r), write (w) and access it (x), users in the group can only read and access the directory, while other users can't do anything. For files the x means execute. 
   ```bash
   drwxr-x--- 2 vision vision 4096 ene 25 18:45 images
   ```
   
   -  ``chmod`` change access permissions of a file (you must have write access)
   -  ``chown`` change the owner of a file
   
## Sample Exercise: Image database

1. Create a folder with your Uniandes username. (If you don't have Linux in your personal computer)

2. Copy *sipi_images* folder to your personal folder. (If you don't have Linux in your personal computer)

3.  Decompress the images (use ``tar``, check the man) inside *sipi_images* folder. 

4.  Use  ``imagemagick`` to find all *grayscale* images. We first need to install the *imagemagick* package by typing

    ```bash
    sudo apt-get install imagemagick
    ```
    
    Sudo is a special command that lets us perform the next command as the system administrator
    (super user). In general it is not recommended to work as a super user, it should only be used 
    when it is necessary. This provides additional protection for the system.
    
    ```bash
    find . -name "*.tiff" -exec identify {} \; | grep -i gray | wc -l
    ```
    
3.  Create a script to copy all *color* images to a different folder
    Lines that start with # are comments
       
      ```bash
      #!/bin/bash
      
      # go to Home directory
      cd ~ # or just cd

      # remove the folder created by a previous run from the script
      rm -rf color_images

      # create output directory
      mkdir color_images

      # find all files whose name end in .tif
      images=$(find sipi_images -name *.tiff)
      
      #iterate over them
      for im in ${images[*]}
      do
         # check if the output from identify contains the word "gray"
         identify $im | grep -q -i gray
         
         # $? gives the exit code of the last command, in this case grep, it will be zero if a match was found
         if [ $? -eq 0 ]
         then
            echo $im is gray
         else
            echo $im is color
            cp $im color_images
         fi
      done
      
      ```
      -  save it for example as ``find_color_images.sh``
      -  make executable ``chmod u+x`` (This means add Execute permission for the user)
      -  run ``./find_duplicates.sh`` (The dot is necessary to run a program in the current directory)
      

## Your turn

1. What is the ``grep``command?

El comando grep se utiliza para buscar cadenas de texto dentro de un archivo. Por su cuenta, lo que hace es buscar el texto      especificado por el usuario dentro de un archivo o directorio, e imprimir las líneas de texto que contienen dicho patrón [1]. Un acercamiento inicial a dicho comando sería  ```$ grep opciones texto_buscado archivo ```, donde en opciones puede especificar las características de la búsqueda a realizar,  texto_buscado es la cadena de caracteres de interés y archivo es el archivo dentro del cual se buscará. Para especificar las características de la búsqueda se utilizan diferentes letras, palabras o símbolos como por ejemplo: -i para ignorar la distinción entre mayúsculas y minúsculas, -c para imprimir el número de coincidencias encontradas, entre otras [2]. 

2. What is the meaning of ``#!/bin/python`` at the start of scripts?

Esta línea de código define el lenguaje de programación y la plataforma en la cual se correrá el script en cuestión. Los símbolos #! (conocidos como shebang) definen que se está trabajando con un archivo ejecutable y permite obviar dicha línea de texto al correr el script [3]. Paso seguido, se pone la ruta del intérprete que se desea utilizar para ejecutar el script; en este caso python, que está en la ruta /bin/python [4]. 

3. Download using ``wget`` the [*bsds500*](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/resources.html#bsds500) image segmentation database, and decompress it using ``tar`` (keep it in you hard drive, we will come back over this data in a few weeks).

Para descargar la base de datos de segmentación de imágenes de Berkeley se utiliza el comando wget que recibe el link de descarga de la base de datos como se muestra a continuación:  ```wget http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/BSR/BSR_bsds500.tgz]. Después, para descomprimir el archivo se utiliza el comando [tar xzvf BSR_bsds500.tgz ``` [5]. 
 
4. What is the disk size of the uncompressed dataset, How many images are in the directory 'BSR/BSDS500/data/images'?

Para encontrar el tamaño en disco de la base de datos se utiliza el comando [du -sh BSR], dando como resultado 73MB. En este caso se utilizaron dos opciones: -h para poder visualizar las unidades de la información y -s para no tener en cuenta subdirectorios sino únicamente el tamaño de BSR [6]. Por otro lado, para hallar el número de imágenes del directorio de interés, es decir 500 imágenes, se puede utilizar un comando muy similar al ejemplo de las imágenes a escala de grises:  ```find ./BSR/BSDS500/data/images -name "*.jpg" -exec identify {} \; | wc -l ```. 
 
5. What are all the different resolutions? What is their format? Tip: use ``awk``, ``sort``, ``uniq`` 

Para resolver este numeral se utilizó lo aprendido anteriormente, el comando awk cuyo lenguaje permite manipular de forma más sencilla cadenas de texto, sort para ordenar los datos obtenidos y uniq para eliminar duplicados. Debido a que el resultado del comando identify es una cadena de texto que muestra las características de un archivo, se puede utilizar el lenguaje awk para imprimir sólo las palabras que contienen los datos de interés de las imágenes, en este caso la resolución y formato. Posteriormente se ordenan las palabras obtenidas y se borran los duplicados para obtener sólo los resultados que no se repiten [7].


6. How many of them are in *landscape* orientation (opposed to *portrait*)? Tip: use ``awk`` and ``cut``

Para encontrar el número de imágenes con orientación de paisaje, es decir que se ven horizontales, se tuvo en cuenta la resolución hallada en el punto anterior y se utilizaron comandos conocidos como find, identify, awk, grep y wc. Sabiendo que las imágenes con la orientación de interés eran las que tenían una resolución de 481x321, se buscó el número de imágenes que tenían dicha resolución, como se muestra a continuación:  ```find ./BSR/BSDS500/data/images -name "*.jpg" -exec identify {} \; | awk '{print $3}' | grep '481x321'| wc -l ```. 
La parte del comando awk podría ser reemplazada por  ```cut -d ‘ ‘ -f 3 ```, donde se estaría extrayendo la tercera palabra delimitada por espacios, o también se podría buscar las imágenes poniendo como delimitador la ‘x’ y buscando un único número de la resolución. Finalmente se encontró que hay 348 imágenes con orientación de paisaje, y si se intercambian los números de la resolución, se muestra que hay 152 imágenes con la orientación de retrato.

 
7. Crop all images to make them square (256x256) and save them in a different folder. Tip: do not forget about  [imagemagick](http://www.imagemagick.org/script/index.php).

   Para completar este punto, se utilizó el script que se muestra en la parte inferior. En este, primero se creó una nueva carpeta llamada ‘crop’, utilizando el comando  ```mkdir crop ```, dentro de la carpeta de imágenes. Para simplificar el proceso lo que se hizo fue copiar todas las imágenes a esta nueva carpeta y luego si se realizó el corte, recorriendo cada una de las imágenes del directorio [8].

 ```
#!/bin/bash

# Go to the image directory
cd .*/BSR/BSDS500/data/images

# Remove the folder created by the previous run
rm -rf crop

# Create the new output directory
mkdir crop

# Copy all the files ending in .jpg into the output directory
cp -r $(find . -name "*.jpg") ./crop

#  Find all the images of the output directory
images=$(find ./crop -name *jpg)

# Iterate over the images found
for im in ${images[*]}
do

# Crop every image , identifying each of them by their original name
convert $(identify $im | awk '{print $1}') -gravity center -crop 256x256+0+0 $($

done
 ```
 
# References

1. https://www.computerhope.com/unix/ugrep.htm
2. https://www.cyberciti.biz/faq/howto-use-grep-command-in-linux-unix/
3. https://stackoverflow.com/questions/2429511/why-do-people-write-the-usr-bin-env-python-shebang-on-the-first-line-of-a-pyt
4. http://docs.python.org.ar/tutorial/3/interpreter.html
5. https://www.linuxtotal.com.mx/?cont=info_admon_004
6. https://www.geeksforgeeks.org/du-command-linux-examples/
7. http://www.sromero.org/wiki/linux/aplicaciones/uso_de_awk
8 https://imagemagick.org/Usage/crop/#crop



# Report

For every question write a detailed description of all the commands/scripts you used to complete them. DO NOT use a graphical interface to complete any of the tasks. Use screenshots to support your findings if you want to. 

Feel free to search for help on the internet, but ALWAYS report any external source you used.

Notice some of the questions actually require you to connect to the course server, the login instructions and credentials will be provided on the first session. 

## Deadline

We will be delivering every lab through the [github](https://github.com) tool (Silly link isn't it?). According to our schedule we will complete that tutorial on the second week, therefore the deadline for this lab will be specially long **February 7 11:59 pm, (it is the same as the second lab)** 

### More information on

http://www.ee.surrey.ac.uk/Teaching/Unix/ 




