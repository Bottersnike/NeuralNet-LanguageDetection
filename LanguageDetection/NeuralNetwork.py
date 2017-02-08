import random
from Brain import Brain
import time
import os


class NeuralNetwork(object):
    MINIMUM_WORD_LENGTH = 5
    STARTING_AXON_VARIABILITY = 1.0
    TRAINS_PER_FRAME = 20
    LANGUAGE_COUNT = 13
    MIDDLE_LAYER_NEURON_COUNT = 19
    SAMPLE_LENGTH = 15
    INPUTS_PER_CHAR = 27
    INPUT_LAYER_HEIGHT = INPUTS_PER_CHAR * SAMPLE_LENGTH + 1
    OUTPUT_LAYER_HEIGHT = LANGUAGE_COUNT + 1
    RESULT_CELL_LENGTH = 12

    def __init__(self):
        self.training_data = [[] for i in range(self.LANGUAGE_COUNT)]
        self.line_at = 0
        self.iteration = 0
        self.guess_window = 1000
        self.recent_guesses = [False for i in range(self.guess_window)]
        self.recent_right_count = 0
        self.training = True
        self.word = "-"
        self.desired_output = 0

        self.counted_languages = [0, 1]
        self.last_one_was_correct = False
        self.languages = ["Random", "Key Mash", "English", "Spanish", "French", "German", "Japanese", "Swahili",
                          "Mandarin", "Esperanto", "Dutch", "Polish", "Lojban"]
        self.lang_sizes = [0 for i in range(self.LANGUAGE_COUNT)]

        self.long_term_results = [[0 for i in range(self.LANGUAGE_COUNT)] for i in range(self.LANGUAGE_COUNT)]
        self.log_number = 0

        self.streak = 0
        self.long_streak = 0

        self.smooth = 0

        self.error = 0
        self.brain = None

    def setup(self):
        for i in range(self.LANGUAGE_COUNT):
            self.training_data[i] = open(os.path.dirname(os.path.realpath(__file__)) + "/data/output%d.txt" % i, "r").read().splitlines()
            s = self.training_data[i][len(self.training_data[i]) - 1]
            self.lang_sizes[i] = int(s.split(",")[1])

        for i in range(self.guess_window):
            self.recent_guesses[i] = False

        bls = [self.INPUT_LAYER_HEIGHT, self.MIDDLE_LAYER_NEURON_COUNT, self.OUTPUT_LAYER_HEIGHT]
        self.brain = Brain(bls, self.INPUTS_PER_CHAR, self.languages, self.STARTING_AXON_VARIABILITY)

    def draw(self):
        if self.training:
            for i in range(self.TRAINS_PER_FRAME):
                self.train()

        print "Iteration #%d" % self.iteration
        print "Input word:", self.word.upper()
        print "Expected output:",
        o = self.languages[self.desired_output]
        if typing:
            o = "???"
        print o
        print "Step size:", self.brain.alpha
        print "Actual prediction:",
        if typing:
            s = "HOW'D I DO?"
        else:
            if self.last_one_was_correct:
                s = "RIGHT"
            else:
                s = "WRONG"
        print self.languages[self.brain.top_output], "(" + s + ")"
        print "Confidence:", self.percentify(self.brain.confidence)
        print "%% of last %d correct:" % self.guess_window,
        print self.percentify(100.0 * ((1.0 * self.recent_right_count) / min(self.iteration, self.guess_window)))
        print "Current streak:", self.streak
        print "Longest streak:", self.long_streak

        return True

    def train(self):
        lang = random.choice(self.counted_languages)
        self.word = ""

        while len(self.word) < self.MINIMUM_WORD_LENGTH:
            word_index = random.randint(0, self.lang_sizes[lang])
            self.line_at = self.binary_search(lang, word_index) - 1
            parts = self.training_data[lang][self.line_at].split(",")
            self.word = parts[0]

        self.desired_output = lang
        self.error = self.get_brain_error_from_line(self.word, self.desired_output, True)
        if self.brain.top_output == self.desired_output:
            if not self.recent_guesses[self.iteration % self.guess_window]:
                self.recent_right_count += 1

            self.recent_guesses[self.iteration % self.guess_window] = True
            self.last_one_was_correct = True
            self.streak += 1
        else:
            if self.recent_guesses[self.iteration % self.guess_window]:
                self.recent_right_count -= 1

            self.recent_guesses[self.iteration % self.guess_window] = False
            self.last_one_was_correct = False
            if self.streak > self.long_streak:
                self.long_streak = self.streak

            self.streak = 0
            self.long_term_results[self.brain.top_output][self.desired_output] += 1

    def binary_search(self, lang, n):
        return self.binary_search_(lang, n, 0, len(self.training_data[lang]) - 1)

    def binary_search_(self, lang, n, beg, end):
        if beg > end:
            return beg

        mid = (beg + end) / 2

        s = self.training_data[lang][mid]
        diff = n - int(s.split(",")[1])

        if diff == 0:
            return mid + 1
        elif diff > 0:
            return self.binary_search_(lang, n, mid + 1, end)
        elif diff < 0:
            return self.binary_search_(lang, n, beg, mid - 1)

        return -1

    @staticmethod
    def percentify(d):
        return str(round(d, 1)) + "%"

    def get_brain_error_from_line(self, word, desired_output, do_train):
        inputs = [0.0 for i in range(self.INPUT_LAYER_HEIGHT)]

        for i in range(self.SAMPLE_LENGTH):
            c = 0
            if i < len(word):
                c = ord(word.upper()[i]) - 64
            c = max(0, c)
            inputs[i * self.INPUTS_PER_CHAR + c] = 1

        desired_outputs = [0.0 for i in
                           range(self.OUTPUT_LAYER_HEIGHT)]

        desired_outputs[desired_output] = 1
        if do_train:
            self.iteration += 1

        return self.brain.use_brain_get_error(inputs, desired_outputs, do_train)


def output_log(name):
    """PrintWriter results = null;
  try{
        int amountCorrect=0;
        int numberOfTimes;
        double percentageOfTimes;
        String resultLine;
        results = createWriter("results/"+name+".txt");
        int spacesNeeded;

        for(int t = 0; t<RESULT_CELL_LENGTH; t++){
          results.print(" ");

          //System.out.print(" ");
        }

        for(int i = 0; i<LANGUAGE_COUNT; i++){
          results.print(languages[i]);
          //System.out.print(languages[i]);
          spacesNeeded = RESULT_CELL_LENGTH-languages[i].length();

          for(int t = 0; t<spacesNeeded; t++){
            results.print(" ");

            //System.out.print(" ");
          }
        }

        results.println();
        results.println();

        //System.out.println();
        //System.out.println();

        for(int given = 0; given < LANGUAGE_COUNT; given++){
          results.print(languages[given]);

          //System.out.print(languages[given]);
          spacesNeeded = RESULT_CELL_LENGTH-languages[given].length();

          for(int t = 0; t<spacesNeeded; t++){
            results.print(" ");

            //System.out.print(" ");
          }
          for(int answer = 0; answer < LANGUAGE_COUNT; answer++){

            numberOfTimes = longTermResults[answer][given];
            percentageOfTimes = round(((double)numberOfTimes) / ((double)iteration) * 100, 2);
            resultLine = percentageOfTimes + "%";
            results.print(resultLine);

           // System.out.print(resultLine);

            spacesNeeded = RESULT_CELL_LENGTH-resultLine.length();
            for(int t = 0; t<spacesNeeded; t++){
              results.print(" ");

             // System.out.print(" ");
            }

            if(answer == given){
              amountCorrect += numberOfTimes;
            }
          }
          results.println();
          //System.out.println();
        }

        double percentageCorrect = round(((double)amountCorrect) / ((double)iteration) * 100, 2);
        results.println(percentageCorrect + "% Correct");
        results.println("Longest Streak:"+longStreak);
        results.println("Iteration #" + iteration);

        //System.out.println(percentageCorrect + "% Correct");
        //System.out.println("Longest Streak:"+longStreak);
        //System.out.println("Iteration #" + iteration);



      }catch(Exception e){
        System.out.println(e.toString());
      }
      finally{
        if(results != null){
          results.flush();
          results.close();
        }
      }"""


if __name__ == "__main__":
    network = NeuralNetwork()
    network.setup()

    frame_rate = 200
    target_speed = 1.0 / frame_rate
    running = True

    while running:
        print "Running..."
        frame_start = time.time()

        running = network.draw()

        frame_end = time.time()
        delta_time = frame_end - frame_start
        if delta_time < target_speed:
            time.sleep(target_speed - delta_time)
