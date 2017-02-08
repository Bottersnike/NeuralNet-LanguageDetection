from stdlib import Map
import random
import math


class Brain(object):
    def __init__(self, bls, ipc, lang, starting_axon_variability=1.0):
        self.neurons = Map()  # 2D
        self.axons = Map()  # 3D
        self.BRAIN_LAYER_SIZES = bls
        self.MAX_HEIGHT = 0
        self.condenseLayerOne = True
        self.draw_width = 5
        self.alpha = 0.1
        self.confidence = 0.0
        self.INPUTS_PER_CHAR = ipc  # Int
        self.languages = lang
        self.top_output = 0
        self.STARTING_AXON_VARIABILITY = starting_axon_variability

        for x in range(len(self.BRAIN_LAYER_SIZES)):
            if self.BRAIN_LAYER_SIZES[x] > self.MAX_HEIGHT:
                self.MAX_HEIGHT = self.BRAIN_LAYER_SIZES[x]

            self.neurons[x] = [self.BRAIN_LAYER_SIZES[x]]

            for y in range(self.BRAIN_LAYER_SIZES[x]):
                if y == self.BRAIN_LAYER_SIZES[x] - 1:
                    self.neurons[x, y] = 1
                else:
                    self.neurons[x, y] = 0

            if x < len(self.BRAIN_LAYER_SIZES) - 1:
                for y in range(self.BRAIN_LAYER_SIZES[x]):
                    for z in range(self.BRAIN_LAYER_SIZES[x + 1]):
                        starting_weight = (random.random() * 2 - 1) * self.STARTING_AXON_VARIABILITY
                        self.axons[x, y, z] = starting_weight

    def use_brain_get_error(self, inputs, desired_outputs, mutate):
        nonzero = [self.BRAIN_LAYER_SIZES[0] - 1]

        for i in range(self.BRAIN_LAYER_SIZES[0]):
            self.neurons[0, i] = inputs[i]
            if inputs[i] != 0:
                nonzero.append(i)

        for x in range(len(self.BRAIN_LAYER_SIZES)):
            self.neurons[x, self.BRAIN_LAYER_SIZES[x] - 1] = 1.0

        for x in range(1, len(self.BRAIN_LAYER_SIZES)):
            for y in range(self.BRAIN_LAYER_SIZES[x] - 1):
                total = 0
                if x == 1:
                    for i in range(len(nonzero)):
                        total += self.neurons[x - 1, nonzero[i]] * self.axons[x - 1, nonzero[i], y]
                else:
                    for input_ in range(self.BRAIN_LAYER_SIZES[x - 1] - 1):
                        total += self.neurons[x - 1, input_] * self.axons[x - 1, input_, y]
                self.neurons[x, y] = self.sigmoid(total)

        if mutate:
            for y in range(len(nonzero)):
                for z in range(self.BRAIN_LAYER_SIZES[1] - 1):
                    delta = 0
                    for n in range(self.BRAIN_LAYER_SIZES[2] - 1):
                        delta += 2 * (self.neurons[2, n] - desired_outputs[n]) * self.neurons[2, n] * (
                            1 - self.neurons[2, n]) * self.axons[1, z, n] * self.neurons[1, z] * (
                                 1 - self.neurons[1, z]) * \
                                 self.neurons[0, nonzero[y]] * self.alpha
                    self.axons[0, nonzero[y], z] -= delta

            for y in range(self.BRAIN_LAYER_SIZES[1]):
                for z in range(self.BRAIN_LAYER_SIZES[2] - 1):
                    delta = 2 * (self.neurons[2, z] - desired_outputs[z]) * self.neurons[2, z] * (
                        1 - self.neurons[2, z]) * self.neurons[1, y] * self.alpha
                    self.axons[1, y, z] -= delta

        self.top_output = self.get_top_output()
        total_error = 0
        end = len(self.BRAIN_LAYER_SIZES) - 1

        for i in range(self.BRAIN_LAYER_SIZES[end] - 1):
            total_error += math.pow(self.neurons[end, i] - desired_outputs[i], 2)
        return total_error / (self.BRAIN_LAYER_SIZES[end] - 1)

    @staticmethod
    def sigmoid(input_):
        return 1.0 / (1.0 + math.pow(2.71828182846, -input_))

    def get_top_output(self):
        record = -1
        record_holder = -1
        end = len(self.BRAIN_LAYER_SIZES) - 1
        for i in range(self.BRAIN_LAYER_SIZES[end] - 1):
            if self.neurons[end, i] > record:
                record = self.neurons[end, i]
                record_holder = i

        self.confidence = record
        return record_holder

    """ Removed due to Processing specific drawing functions. May replace with Pygame later on.

    public void drawBrain(float scaleUp) {
        final float neuronSize = 0.4;
        noStroke();
        fill(128);
        rect(-0.5 * scaleUp, -0.5 * scaleUp, (BRAIN_LAYER_SIZES.length * drawWidth - 1) * scaleUp, MAX_HEIGHT * scaleUp);
        ellipseMode(RADIUS);
        strokeWeight(3);
        textAlign(CENTER);
        textFont(font, 0.53 * scaleUp);

        for (int x = 0; x < BRAIN_LAYER_SIZES.length - 1; x++) {
            for (int y = 0; y < BRAIN_LAYER_SIZES[x]; y++) {
                for(int z = 0; z < BRAIN_LAYER_SIZES[x+1] - 1; z++){
                    drawAxon(x, y, x + 1, z, scaleUp);
                }
            }
        }

        int startPosition = 0;
        if (condenseLayerOne) {
            for (int y = 0; y < BRAIN_LAYER_SIZES[0]; y++){
                if (neurons[0][y] >= 0.5){
                    noStroke();
                    int ay = apY(0, y);
                    //double val = neurons[0][y]; // not used?
                    fill(255);
                    ellipse(0,ay * scaleUp, neuronSize * scaleUp, neuronSize * scaleUp);
                    fill(0);
                    char c = '-';
                    if (ay == BRAIN_LAYER_SIZES[0] / INPUTS_PER_CHAR) { c = '1'; }
                    else if (y % INPUTS_PER_CHAR >= 1) { c = (char)(y % INPUTS_PER_CHAR + 64); }
                    text(c, 0,( ay + (neuronSize * 0.55)) * scaleUp);
                }
            }
            startPosition = 1;
        }
        for (int x = startPosition; x < BRAIN_LAYER_SIZES.length; x++) {
            for (int y = 0; y < BRAIN_LAYER_SIZES[x]; y++) {
                noStroke();
                double val = neurons[x][y];
                fill(neuronFillColor(val));
                ellipse(x * drawWidth * scaleUp, apY(x, y) * scaleUp, neuronSize * scaleUp, neuronSize * scaleUp);
                fill(neuronTextColor(val));
                text(coolify(val), x * drawWidth * scaleUp, (apY(x, y) + (neuronSize * 0.52)) * scaleUp);
                if (x == BRAIN_LAYER_SIZES.length - 1 && y < BRAIN_LAYER_SIZES[x] - 1) {
                    fill(0);
                    textAlign(LEFT);
                    text(languages[y],(x * drawWidth + 0.7) * scaleUp, (apY(x, y) +( neuronSize * 0.52)) * scaleUp);
                    textAlign(CENTER);
                }
            }
        }
    }
    """

    @staticmethod
    def coolify(val):
        v = int(round(val * 100))
        if v == 100:
            return "1"
        elif v < 10:
            return ".0" + str(v)
        else:
            return "." + str(v)

    """ Removed due to Processing specific drawing functions. May replace with Pygame later on.

    public void drawAxon(int x1, int y1, int x2, int y2, float scaleUp) {
        double v = axons[x1][y1][y2] * neurons[x1][y1];
        if (Math.abs(v) >= 0.001){
            stroke(axonStrokeColor(axons[x1][y1][y2]));
            line(x1 * drawWidth * scaleUp, apY(x1, y1) * scaleUp, x2 * drawWidth * scaleUp, apY(x2, y2) * scaleUp);
        }
    }
    """

    def apY(self, x, y):
        if self.condenseLayerOne and x == 0:
            return y / self.INPUTS_PER_CHAR
        else:
            return y

    """ Removed due to Processing specific drawing functions. May replace with Pygame later on.

    public color axonStrokeColor(double d) {
        if (d >= 0) { return color(255, 255, 255, (float)(d * 255)); }
        else { return color(1, 1, 1, abs((float)(d * 255))); }
    }

    public color neuronFillColor(double d) {
        return color((float)(d * 255), (float)(d * 255), (float)(d * 255));
    }

    public color neuronTextColor(double d){
        if (d >= 0.5) { return color(0, 0, 0); }
        else {return color(255, 255, 255); }
    }
    """
