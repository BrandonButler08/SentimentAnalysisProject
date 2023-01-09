REQUIRES PYTHON V3.10

ALL COMMANDS ARE RUN FROM THE DIRECTORY WHERE THE Makefile is present

MAKE FILE PROGRAM INSTALLATION: 
    1. In project directory run "make setup" in terminal

MANUAL INSTALLATION
    1. In project directory run "pip install -r requirements.txt" in terminal

THE PROGRAM OFFERS THREE MODES IN WHICH IT CAN RUN

1. LONG RUN
    a. This mode does testing on 52 reviews, takes about 10mins to finish.
    b. To run type the following in terminal in the project directory : make run_long

2. SHORT RUN
    a. this mode offers a shorter runtime to demo the program, it tests 7 reviews. takes about 2mins to finish.
    b. to run type the following in terminal in the project directory : make run_short

3. MANUAL RUN
    a. this mode offers manual testing of a single review.
    b. In the manual_test_corpus directory open the "review.txt" and replace the text in the file with the review to be analyzed. 
    MINIMUM 20 words. May fail if to many stop words and not enough feature words included
    c. In the manual_scoring.txt file remove the text within and replace with the same syntax aka: title_of_doc:your_score
    d. to run type the following in terminal in the project directory: make run_manual

RESULTS
    1. Results will be populated in the test_results folder once a run finishes. Test results are overwritten every run.
        a. results_1.html
            i. this is a scatter plot of all words scored during the test, anything above a zero is considered positive and vice versa for negative.
                The graph provides tools for zooming in if you want to see a specific area better.
        b. results_2.html
            i. this is a bar graph of all documents tested, it compares the score gave in the scoring.txt to the score given by the program.
                All scores range from 0-10, 10 being most positive