#!/usr/bin/env python3
import argparse
import random

def generate_strings(N, fuzz_out_dir, corpus_dir, fuzz_loc, san_fuzz_loc, cmp_fuzz_loc):
    base_strings = [""] * N

    # Append AFL_AUTORESUME=1 to all strings
    strings = [string + "AFL_AUTORESUME=1" for string in base_strings]

    # For the final string (N), add 'AFL_FINAL_SYNC=1' at the beginning
    strings[-1] = "AFL_FINAL_SYNC=1 " + strings[-1]

    # Create a dictionary to track used flags for each type
    used_flags = {flag: set() for flag in ["AFL_DISABLE_TRIM", "AFL_KEEP_TIMEOUTS", "AFL_EXPAND_HAVOC_NOW"]}
    used_args = {flag: set() for flag in ["-L 0", "-Z", "-P explore", "-P exploit", "-a binary", "-a ascii"]}

    # Function to append a flag to a random string and update used_flags
    def append_flag(flag, percentage):
        for _ in range(int(N * percentage)):
            index = random.choice(list(set(range(N)) - used_flags[flag]))
            strings[index] += f" {flag}=1"
            used_flags[flag].add(index)

    def append_arg(arg, percentage):
        for _ in range(int(N * percentage)):
            index = random.choice(list(set(range(N)) - used_args[arg]))
            strings[index] += f" {arg}"
            used_args[arg].add(index)


    # Append AFL_DISABLE_TRIM=1 to 65% of strings
    append_flag("AFL_DISABLE_TRIM", 0.65)

    # Append AFL_KEEP_TIMEOUTS=1 to 50% of strings
    append_flag("AFL_KEEP_TIMEOUTS", 0.5)

    # Append AFL_EXPAND_HAVOC_NOW=1 to 40% of strings
    append_flag("AFL_EXPAND_HAVOC_NOW", 0.4)

    strings = [string + " afl-fuzz" for string in strings]

    # Append -L 0 to 10% of strings
    append_arg("-L 0", 0.1)

    # Append -Z to 20% of strings
    append_arg("-Z", 0.2)

    # Append -P explore to 40% of strings
    append_arg("-P explore", 0.4)

    # Append -P exploit to 20% of strings
    append_arg("-P exploit", 0.2)

    # Append -a binary to 30% of strings
    append_arg("-a binary", 0.3)
    # Append -a ascii to 30% of strings
    append_arg("-a ascii", 0.3)

    strings = [string + " -a binary" for string in strings]

    # Cycle through -p $VALUE for the last strings
    power_schedules = ["fast", "explore", "coe", "lin", "quad", "exploit", "rare"]
    for i in range(N):
        strings[i] += f" -p {power_schedules[(i) % len(power_schedules)]}"

    # add -i ~/corpus/
    for i in range(N):
        strings[i] += f" -i {corpus_dir}"

    # add -o ~/fuzz_out/
    for i in range(N):
        strings[i] += f" -o {fuzz_out_dir}"

    # add -S or -M
    strings[N-1] += " -M main"
    for i in range(N-1):
        strings[i] += f" -S main{i+1}"


    # For string N-1, add 'fuzzer-sanitizers'
    strings[N-2] += f" {san_fuzz_loc}"

    # For the rest, 30% add 'fuzzer-cmplog'
    fuzzer_cmplog_count = int(N * 0.3)
    for index in range(fuzzer_cmplog_count):
        # 70% append -l 2, 10% -l 3, and 20% -l 2AT
        rand_num = random.random()
        if rand_num < 0.7:
            strings[index] += " -l 2"
        elif rand_num < 0.8:
            strings[index] += " -l 3"
        else:
            strings[index] += " -l 2AT"
        strings[index] += f" {cmp_fuzz_loc}"

    # For the remaining 70% without 'fuzzer-cmplog' or 'fuzzer-sanitizers', add 'fuzzer'
    for i in range(N):
        if san_fuzz_loc not in strings[i] and cmp_fuzz_loc not in strings[i]:
            strings[i] += f" {fuzz_loc}"

    return strings

def main():
    parser = argparse.ArgumentParser(description="Generate fuzzer configurations.")
    parser.add_argument("-n", "--num-configs", type=int, required=True, help="Number of configurations to generate")
    parser.add_argument("--fuzz-out", type=str, required=True, help="Fuzz output directory")
    parser.add_argument("--corpus", type=str, required=True, help="Corpus directory")
    parser.add_argument("--fuzz-loc", type=str, required=True, help="Location of the main fuzzer binary")
    parser.add_argument("--san-fuzz-loc", type=str, required=True, help="Location of the sanitizers-fuzzer binary")
    parser.add_argument("--cmp-fuzz-loc", type=str, required=True, help="Location of the cmplog-fuzzer binary")

    args = parser.parse_args()

    result_strings = generate_strings(args.num_configs, args.fuzz_out, args.corpus, args.fuzz_loc, args.san_fuzz_loc, args.cmp_fuzz_loc)

    for i, string in enumerate(result_strings, 1):
        print(f"{string}")

if __name__ == "__main__":
    main()
