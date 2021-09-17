# Usage: $python probab1.py initial event nr., expirience level (0-2), no. simulations, distribution in A(1) (optional)
from reliability.Distributions import Weibull_Distribution, Normal_Distribution
import numpy as np
import csv
import time
import winsound
import sys


def uniform_dist(lo, hi):
    return np.random.uniform(low=lo, high=hi, size=ev_nr)


def exp_dist(med):
    return np.random.exponential(1/med, ev_nr)


def normal_dist(med):
    norm_dist = Normal_Distribution(med, 1)
    return norm_dist.random_samples(ev_nr)


def level_rasm(level=2):  # Expirience level according to Rasmussen
    if level == 2 or level == "skill":
        return skill_dist.random_samples(ev_nr)
    elif level == 1 or level == "rule":
        return rule_dist.random_samples(ev_nr)
    elif level == 0 or level == "knowledge":
        return knowledge_dist.random_samples(ev_nr)


def dh_p(t):
    if t < 2:
        return 5*(t**2)/2  # Accelerating to stall w
    else:
        return 10*t  # Falling velocity (w1) in stall 10 m/s


def dh_k(t):
    return 20*t  # Falling velocity in stall spin 20 m/s


def z_k2(h, c):
    if c == 2:
        return min((h/10) * 1, 1)
    if c == 3:
        return min((h / 10) * 0.8, 0.8)
    if c == 4:
        return min((h / 10) * 0.4, 0.4)


def dh_hol(t):
    return 3.5*t


def relese_ev_a2(h):  # Field landing probability
    if 40 < h <= 60:
        q_field = 0.05 * h - 2
    elif 60 < h <= 90:
        q_field = 1
    elif 90 < h <= 120:
        q_field = -(1 / 30) * h + 4
    else:
        q_field = 0
    relese = np.random.choice(np.arange(1, 3), p=[1 - q_field, q_field])
    return relese


def end_message():
    print("Done simulating event A(" + str(a) + "), on expirience level " + str(tp1_level) +
          ", with n =", str(ev_nr), "of samples.")
    print("Paths probabilities:", events)


if __name__ == "__main__":
    # Checking for command line arguments
    if len(sys.argv) == 4 and 0 <= int(sys.argv[2]) <= 2 and 1 <= int(sys.argv[1]) <= 6:
        a = int(sys.argv[1])
        tp1_level = int(sys.argv[2])
        ev_nr = int(sys.argv[3])
        b = 1  # Default
    elif len(sys.argv) == 5 and 0 <= int(sys.argv[2]) <= 2 and 1 <= int(sys.argv[1]) <= 6\
            and 0 <= int(sys.argv[1]) <= 4:
        a = int(sys.argv[1])
        tp1_level = int(sys.argv[2])
        ev_nr = int(sys.argv[3])
        b = int(sys.argv[4])
    else:  # For compiler launch, manualy change values below
        print("Incorret arguments, setting default")
        tp1_level = 2  # Expirience level for tp1 (0-2)
        a = 4  # Initial event
        # Distribution for A(1) event, 1 - Weibull, 2 - Uniform, 3 - Expotential, 4 - Normal(Gaussian)
        b = 1
        ev_nr = 10 ** 5  # Number of simulations
    # Runtime measure
    start_time = time.time()

    teta = {"skill": 0.388, "rule": 1.14, "knowledge": 0.969}  # In reliability lib, teta is alfa
    beta = {"skill": 1.13, "rule": 1.27, "knowledge": 0.795}
    gamma = {"skill": 0.072, "rule": 0.148, "knowledge": 0.389}

    # Skill, rule and knowledge based distriibutions
    skill_dist = Weibull_Distribution(alpha=teta['skill'], beta=beta['skill'], gamma=gamma['skill'])
    rule_dist = Weibull_Distribution(alpha=teta['rule'], beta=beta['rule'], gamma=gamma['rule'])
    knowledge_dist = Weibull_Distribution(alpha=teta['knowledge'], beta=beta['knowledge'], gamma=gamma['knowledge'])

    # Aerotow events
    if a == 1:  # Lost direction in initial start phase
        events = [0, 0, 0, 0, 0, 0, 0]
        if b == 1:  # Weibull distribution
            # Samples of reaction times
            tp1 = 5 * level_rasm(tp1_level)
            tp2 = 5 * rule_dist.random_samples(ev_nr)
            tk = 7 * rule_dist.random_samples(ev_nr)
            th = 7 * knowledge_dist.random_samples(ev_nr)
            tkr = 12
            print("Done sampling")
        elif b == 2:  # Uniform distribution
            # Samples of reaction times
            tp1 = uniform_dist(2, 6)
            tp2 = uniform_dist(2, 8)
            tk = uniform_dist(4, 10)
            th = uniform_dist(4, 10)
            tkr = 12
            print("Samples:", tp1[0], tp2[0], tk[0], th[0])
        elif b == 3:  # Exp distribution
            # Samples of reaction times, input subtracted by shift
            tp1 = exp_dist(2) + 2
            tp2 = exp_dist(3) + 2
            tk = exp_dist(3) + 4
            th = exp_dist(3) + 4
            tkr = 12
            print("Samples:", tp1[0], tp2[0], tk[0], th[0])
        elif b == 4:  # Normal distribution
            # Samples of reaction times
            tp1 = normal_dist(4)
            tp2 = normal_dist(5)
            tk = normal_dist(7)
            th = normal_dist(7)
            tkr = 12
            print("Samples:", tp1[0], tp2[0], tk[0], th[0])
        else:
            print("Invalid input value b")
            sys.exit()
        # Samples of arbitrary probability based items
        spilot_release = np.random.choice(np.arange(1, 3), ev_nr, p=[0.05, 0.95])
        tpilot_release = np.random.choice(np.arange(1, 3), ev_nr, p=[0.15, 0.85])
        line_break = np.random.choice(np.arange(1, 3), ev_nr, p=[0.6, 0.4])
        for i in range(ev_nr):
            # Asuring user the program is running
            if i % (ev_nr/100) == 0:
                print("Test number:", i)
            # Event tree conditions
            if tp1[i] < tk[i]:
                end_event = 1  # Line relese, and normal stop
            else:  # Glider pilot's reaction after director
                if tp2[i] < th[i] and tk[i]+tp2[i] < tkr:
                    if spilot_release[i] == 1:
                        end_event = 2  # Ground spin
                    else:
                        end_event = 3  # Normal stop
                elif tk[i]+th[i] < tkr:
                    if tpilot_release[i] == 1:
                        end_event = 4  # Ground spin
                    else:
                        end_event = 5  # Normal stop
                else:
                    if line_break[i] == 1:
                        end_event = 6    # Ground spin
                    else:
                        end_event = 7  # Normal stop
            events[end_event-1] += 1
        events = [n / ev_nr for n in events]
        end_message()
    if a == 2:  # Tow plane power loss
        f = open("a2.csv", "w", newline="")
        writer = csv.writer(f)
        header = ["h", "1", "2", "3", "Z(c2)", "Z(c3)", "Z(c4)"]
        writer.writerow(header)
        # Samples of reaction times
        tp1 = 3 * level_rasm(tp1_level)
        tp2 = 3 * rule_dist.random_samples(ev_nr)
        tk = 6 * rule_dist.random_samples(ev_nr)
        th1 = 4 * rule_dist.random_samples(ev_nr)
        th2 = 4 * skill_dist.random_samples(ev_nr)
        # Samples of arbitrary probability based items
        no_relese = np.random.choice(np.arange(1, 3), ev_nr, p=[0.5, 0.5])
        for h_break in range(0, 305, 5):
            events = [0, 0, 0]
            z = [0, 0, 0]
            for i in range(ev_nr):
                # Asuring user the program is running
                if i % (ev_nr / 100) == 0:
                    print("Test number:", i)
                # Chceking who reacts first, director or tow pilot
                tr = min(tk[i], th1[i])
                # Event tree conditions
                if tp1[i] < tr:
                    end_event = relese_ev_a2(h_break - dh_hol(tp1[i]))
                else:
                    if h_break < dh_hol(tr + min(tp2[i], th2[i])):
                        end_event = 3
                    elif tp2[i] < th2[i]:
                        end_event = relese_ev_a2(h_break - dh_hol(tr + tp2[i]))
                    else:
                        end_event = relese_ev_a2(h_break - dh_hol(tr + th2[i]))
                events[end_event - 1] += 1
            events = [n / ev_nr for n in events]
            # Danger estimation z[0]=z(c2)
            z[0] = events[1] * 0.6 + events[2] * 0.04
            z[1] = events[1] * 0.3 + events[2] * 0.01
            z[2] = events[1] * 0.1 + events[2] * 0

            events.append(z[0])
            events.append(z[1])
            events.append(z[2])
            events.insert(0, h_break)
            writer.writerow(events)
            end_message()
        f.close()
    if a == 3:  # No relese after signal from tow pilot
        events = [0, 0, 0, 0]
        # Samples of reaction times
        tp1 = 3 * rule_dist.random_samples(ev_nr)
        tk = 5 * rule_dist.random_samples(ev_nr)
        th1 = 4 * rule_dist.random_samples(ev_nr)
        th2 = 4 * rule_dist.random_samples(ev_nr)
        tkr = 8
        # Samples of arbitrary probability based items
        no_reaction = np.random.choice(np.arange(1, 3), ev_nr, p=[0.7, 0.3])
        print("Done sampling")
        for i in range(ev_nr):
            # Asuring user the program is running
            if i % (ev_nr / 100) == 0:
                print("Test number:", i)
            # Chceking who reacts first, director or tow pilot
            tr = min(tk[i], th1[i])
            # Event tree conditions
            if tp1[i] < th2[i] and tr+tp1[i] < tkr:
                end_event = 1  # Line relesed by glider
            elif tp1[i] > th2[i] and tr + th2[i] < tkr:
                end_event = 2  # Line relesed by tow pilot
            else:
                if no_reaction[i] == 1:
                    end_event = 3
                else:
                    end_event = 4
            events[end_event - 1] += 1
        events = [n / ev_nr for n in events]
        end_message()
    # Winch tow events
    if a == 4:  # Direction loss in initial start phase
        events = [0, 0, 0, 0]
        # Samples of reaction times
        tp1 = 3 * level_rasm(tp1_level)
        tp2 = 3 * rule_dist.random_samples(ev_nr)
        tk = 4 * rule_dist.random_samples(ev_nr)
        tkr = 6
        # Samples of arbitrary probability based items
        spilot_release = np.random.choice(np.arange(1, 3), ev_nr, p=[0.1, 0.9])
        print("Done sampling")
        for i in range(ev_nr):
            # Asuring user the program is running
            if i % (ev_nr / 100) == 0:
                print("Test number:", i)
            # Event tree conditions
            if tp1[i] < tk[i]:
                end_event = 1
            elif tp2[i]+tk[i] < tkr:
                if spilot_release[i] == 1:
                    end_event = 2
                else:
                    end_event = 3
            else:
                end_event = 4

            events[end_event - 1] += 1
        events = [n / ev_nr for n in events]
        end_message()
    if a == 5:  # Line break
        f = open("a5.csv", "w", newline="")
        writer = csv.writer(f)
        header = ["h", "1", "2", "3", "4", "5", "6", "7", "8", "Z(c2)", "Z(c3)", "Z(c4)"]
        writer.writerow(header)
        h3 = 50

        # Samples of reaction times
        tp1 = 3 * level_rasm(tp1_level)
        tp2 = 4 * rule_dist.random_samples(ev_nr)
        tp3 = 4 * rule_dist.random_samples(ev_nr)
        tk1 = 6 * rule_dist.random_samples(ev_nr)
        tkr = 4
        print("Done sampling")

        for h_break in range(0, 305, 5):
            events = [0, 0, 0, 0, 0, 0, 0, 0]
            z = [0, 0, 0]
            for i in range(ev_nr):
                # Asuring user the program is running
                if i % (ev_nr / 100) == 0:
                    print("Test number:", i)

                # Event tree conditions
                if tp1[i] < tkr and h_break > dh_p(tp1[i]):
                    end_event = 1
                elif h_break < dh_p(tp1[i]) and h_break < dh_p(tkr):
                    end_event = 2
                else:
                    if tp2[i] < tk1[i]:
                        if h_break > dh_p(tkr) + dh_k(tp2[i]) + h3:
                            end_event = 3
                        elif h_break > dh_p(tkr) + dh_k(tp2[i]):
                            end_event = 4
                        else:
                            end_event = 5
                    else:
                        if h_break > dh_p(tkr) + dh_k(tp3[i]) + h3:
                            end_event = 6
                        elif h_break > dh_p(tkr) + dh_k(tp3[i]):
                            end_event = 7
                        else:
                            end_event = 8
                events[end_event - 1] += 1
            events = [n/ev_nr for n in events]
            # Danger estimation z[0]=z(c2)
            z[0] = events[1] * z_k2(h_break, 2) + (events[3] + events[6]) * 1 + (events[4] + events[7]) * 0.9
            z[1] = events[1] * z_k2(h_break, 3) + (events[3] + events[6]) * 1 + (events[4] + events[7]) * 0.8
            z[2] = events[1] * z_k2(h_break, 4) + (events[3] + events[6]) * 1 + (events[4] + events[7]) * 0.6
            events.insert(0, h_break)
            events.append(z[0])
            events.append(z[1])
            events.append(z[2])

            writer.writerow(events)
            end_message()
        f.close()
    if a == 6:  # No relese at the end of winch tow
        events = [0, 0, 0, 0, 0]
        # Samples of reaction times
        tp1 = 4 * rule_dist.random_samples(ev_nr)
        tw = 6 * rule_dist.random_samples(ev_nr)
        tk1 = 5 * rule_dist.random_samples(ev_nr)
        tkr = 9
        # Samples of arbitrary probability based items
        no_relese = np.random.choice(np.arange(1, 3), ev_nr, p=[0.9, 0.1])
        print("Done sampling")
        for i in range(ev_nr):
            # Asuring user the program is running
            if i % (ev_nr / 100) == 0:
                print("Test number:", i)

            # Event tree conditions
            if tw[i] < tk1[i]:
                end_event = 1
            else:
                if tp1[i]+tk1[i] < tkr or tw[i] < tkr:
                    if tp1[i]+tk1[i] < tw[i]:
                        end_event = 2
                    else:
                        end_event = 3
                else:
                    if no_relese[i] == 1:
                        end_event = 4
                    else:
                        end_event = 5
            events[end_event - 1] += 1
        events = [n / ev_nr for n in events]
        end_message()

    # Sound notification at the end of the programe
    print("Runing time:", (time.time() - start_time))
    winsound.MessageBeep(-1)
