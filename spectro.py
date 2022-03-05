import matplotlib.pyplot as plt
import capture
import process
import sys

if __name__ == '__main__':
    argument_list = sys.argv[1:]
    try:
        arg = argument_list[0]
    except:
        print("Atleast one argument required!")
        exit()

    if arg in ("-h", "--help"):
        print(
        '''Commands:
                -h, --help            display information about commands
                -c, --callibrate      callibrate data using reference image #
                -i, --image           display camera feed and input device #; press 'c' to capture; press 'q' to quit
                -p, --plot            pull data from given image name and display graph
                -d, --delete          delete specific image by name, '-1' to delete all images
                -a, --process         process image in pics/ to a .csv in data/
                -s, --stack           stack plots into one, list all names in stack
        '''
        )
    elif arg in ("-c", "--callibrate"):
        process.callibrate(argument_list[1])
    elif arg in ("-i", "--picture"):
        if len(argument_list) != 3:
            print("Error: two arguments needed: filename & device number")
        else:
            try:
                filename = capture.capture_image(argument_list[1], int(argument_list[2]))
                if filename != -1:
                    process.process_image(filename)
            except:
                print("Error processing picture, try again.")
    elif arg in ("-p", "--plot"):
        try:
            process.set_plot(argument_list[1])
            plt.legend()
            plt.show()
            print("Use the save icon to save the plot as a png.")
        except:
            print("Error finding picture data.")
    elif arg in ("-d", "--delete"):
        try:
            process.delete(argument_list[1])
        except:
            print("Error: input name of an existing file to delete or '-1' to delete all files.")
    elif arg in ("-a", "--process"):
        try:
            process.process_image(argument_list[1] + '.png')
        except:
            print("Error locating file")
    elif arg in ("-s", "--stack"):
        for i in range(1, len(argument_list)):
            process.set_plot(argument_list[i])
        plt.legend()
        plt.show()