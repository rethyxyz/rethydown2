import re
import os
import sys

MASTER_FILENAME = "rethydown2"
DESCRIPTION = "A template-based static site generator (v2.0)."
PROJECT_LINK = "https://github.com/rethyxyz/rethydown2"

OPEN_TOKEN = "{|"
CLOSE_TOKEN = "|}"

DEST_FILE_EXT = ".html"

def MOTD():
    print(f"{MASTER_FILENAME}: {DESCRIPTION}")
    print("rethy.xyz (C) 2023")
    print("")
def Version():
    print(f"Past versions can be found at {PROJECT_LINK}.")
    print("")

def Main():
    # Display MOTD text, and description/disclaimer.
    MOTD()

    # Display current build version and project link.
    Version()

    # -------------- #
    # INIT VARIABLES #
    # -------------- #

    # Depending on the state of the input file, we might make the tags. The
    # states here will be changed after if found to be true.
    createHTML = False
    createHead = False
    createBody = False

    outputFileNames = []

    # Basic iterators.
    lineCounter = 0
    fileCounter = 0

    # -------------- #
    # LOOP ARGS LIST #
    # -------------- #

    for inputFileName in sys.argv[1:]:
        # NULLification.
        outputFileLines = []

        # outputFileName is equal to ((inputFileName - ext) + DEST_FILE_EXT)
        outputFileName = os.path.splitext(inputFileName)[0] + DEST_FILE_EXT

        # Check if the source file exists.
        if not os.path.isfile(inputFileName):
            print(f"[ERROR] \"{inputFileName}\" doesn't exist.")
            print("")
            continue

        # Read all lines of inputFileName as inputFileLines variable.
        with open(inputFileName, "r") as filePointer:
            try:
                inputFileLines = filePointer.read().splitlines()
            except UnicodeDecodeError:
                print(f"[ERROR] Decode error on \"{inputFileName}\".")
                print("")
                continue

        # --------------- #
        # LOOP FILE LINES #
        # --------------- #

        for line in inputFileLines:
            # Iterate the line here so it doesn't get skipped.
            lineCounter += 1

            embededTagFound = False

            # strip all tabs and whitespace.
            line = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', line, flags=re.M)

            # Skip any form of blank lines, or comments.
            if line.find(OPEN_TOKEN + CLOSE_TOKEN) != -1 or not line:
                continue

            # Look for an OPEN_TOKEN on a line. Recur (not true recursion) until
            # no more tags are found.
            while line.find(OPEN_TOKEN) != -1:
                embededTagFound = True

                # Find the start of the start token.
                tokenStart = line.find(OPEN_TOKEN) + 2
                # Find the start of the end token.
                tokenEnd = line.find(CLOSE_TOKEN)

                # If no end token was found.
                if tokenEnd == -1:
                    print("[ERROR] No closing tag.")
                    print(f"{inputFileName}: Line {lineCounter}")
                    sys.exit(1)

                # Split the string according to token start and end. Take the
                # content between the tags.
                templateFileName = line[tokenStart:tokenEnd]

                # If the template file doesn't exist.
                if not os.path.isfile(templateFileName):
                    print(f"[ERROR] Template \"{templateFileName}\" doesn't exist:")
                    print(f"{inputFileName}: Line {lineCounter}")
                    sys.exit(1)

                # Read the template file content.
                with open(templateFileName, "r") as filePointer:
                    # Replace the template file name and tokens, and replace
                    # with the file content of the template file.
                    line = line.replace(OPEN_TOKEN + templateFileName + CLOSE_TOKEN, filePointer.read().strip())

            # Append the same line as the original to the newly converted file.
            outputFileLines.append(line)

        # If the output file already exists.
        if (os.path.isfile(outputFileName)):
            print(f"[WARNING] Overwritting {outputFileName}")
        else:
            print(f"[WARNING] Creating {outputFileName}")

        outputFileNames.append(outputFileName)

        # lineCounter back to zero.
        lineCounter = 0
        # Setup write access pointer to the outputFileName variable.
        with open(outputFileName, "w") as filePointer:
            for line in outputFileLines:
                print(f"{lineCounter}: {line}")
                # Write to the output file line by line.
                filePointer.write(line + "\n")
                # Iterate the counter.
                lineCounter += 1

        # Print a blank.
        print("")
        # Add to the file counter tally.
        fileCounter += 1

    # Print files processed.
    print(f"[WARNING] Total files processed: {fileCounter}.")
    print(f"[WARNING] {outputFileNames}.")

if __name__ == "__main__":
    Main()
