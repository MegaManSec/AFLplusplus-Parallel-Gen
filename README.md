# AFLplusplus-Parallel-Gen

The `generate.py` script generates commands necessary to run AFL++ using the multi-core options recommended in [the AFL++ documentation](https://aflplus.plus/docs/fuzzing_in_depth/#c-using-multiple-cores) which is based on probabilities / percentages of each fuzzer using each option. The probabilities are as follows:

1. Use AFL_DISABLE_TRIM=1 to 65% of fuzzers,
2. Use AFL_KEEP_TIMEOUTS=1 to 50% of fuzzers,
3. Use AFL_EXPAND_HAVOC_NOW=1 for 40% of fuzzers,
4. Use -L 0 for 10% of fuzzers,
5. Use -Z for 20% of fuzzers,
6. Use -P explore for 40% of fuzzers,
7. Use -P exploit for 20% of fuzzers,
8. Use -a binary for 30% of fuzzers,
9. Use -a ascii for 30% of fuzzers,
10. Use a different -p "fast", "explore", "coe", "lin", "quad", "exploit", "rare" for each fuzzer,
11. Use a fuzzer built with sanitizers for one fuzzer,
12. Use CMLOG fuzzers for 30% of all fuzzers,
13. Of the CMPLOG fuzzers, 70% use -l 2, 10% -l 3, and 20% -l 2AT.
Usage is: `./generate.py -n N --fuzz-out <dir> --corpus <dir> --fuzz-loc <loc> --san-fuzz-loc <loc> --cmp-fuzz-loc <loc>` where `N` is the number of cores you are using, `fuzz_out` is the fuzzing output, `corpus` is the directory with the corpuses, `fuzz-loc` is the location of the binary for fuzzing, `san-fuzz-loc` is the location of the binary which is built with sanitizers, and `cmp-fuzz-loc` is the location of the binary which is built with cmplog. If you're not using sanitizers or cmplog, just set these values t the same as `fuzz-loc`.

---

The `run.sh` script generates commands which can be run to start all of the fuzzers in `screen`:

```bash
$ python3 generate.py -n 32 --fuzz-out "/dev/shm/fuzz" --corpus "/dev/shm/corpus" --fuzz-loc ~/fuzz.bin --san-fuzz-loc ~/fuzz.san.bin --cmp-fuzz-loc ~/fuzz.cmplog.bin  | ./run.sh

screen -dmS screen_main bash -c AFL_FINAL_SYNC=1 AFL_AUTORESUME=1 AFL_DISABLE_TRIM=1 AFL_KEEP_TIMEOUTS=1 afl-fuzz -a binary -p lin -i /dev/shm/corpus -o /dev/shm/fuzz -M main /Users/opera_user/fuzz.bin; exec bash
screen -dmS screen_main1 bash -c AFL_AUTORESUME=1 afl-fuzz -P explore -P exploit -a binary -a binary -p fast -i /dev/shm/corpus -o /dev/shm/fuzz -S main1 -l 2 /Users/opera_user/fuzz.cmplog.bin; exec bash
screen -dmS screen_main2 bash -c AFL_AUTORESUME=1 AFL_DISABLE_TRIM=1 afl-fuzz -P explore -a binary -a binary -p explore -i /dev/shm/corpus -o /dev/shm/fuzz -S main2 -l 2 /Users/opera_user/fuzz.cmplog.bin; exec bash
.....
```

You can therefore just run
```bash
$ python3 generate.py -n 32 --fuzz-out "/dev/shm/fuzz" --corpus "/dev/shm/corpus" --fuzz-loc ~/fuzz.bin --san-fuzz-loc ~/fuzz.san.bin --cmp-fuzz-loc ~/fuzz.cmplog.bin  | ./run.sh | bash
```
to execute everything.
