#!/usr/bin/env bash

time pheniqs mux --config SRR6750041_first_adjusted.json --report SRR6750041_second_report.json --prior SRR6750041_second_adjusted.json --output SRR6750041_decoded.cram
time pheniqs mux --config SRR6750056_first_adjusted.json --report SRR6750056_second_report.json --prior SRR6750056_second_adjusted.json --output SRR6750056_decoded.cram
time pheniqs mux --config SRR6750057_first_adjusted.json --report SRR6750057_second_report.json --prior SRR6750057_second_adjusted.json --output SRR6750057_decoded.cram
time pheniqs mux --config SRR6750058_first_adjusted.json --report SRR6750058_second_report.json --prior SRR6750058_second_adjusted.json --output SRR6750058_decoded.cram
time pheniqs mux --config SRR6750059_first_adjusted.json --report SRR6750059_second_report.json --prior SRR6750059_second_adjusted.json --output SRR6750059_decoded.cram

# real    4m8.614s
# user    84m29.555s
# sys     7m25.276s
#
# real    11m40.550s
# user    240m11.549s
# sys     20m20.187s
#
# real    11m19.723s
# user    234m9.310s
# sys     19m10.309s
#
# real    11m38.087s
# user    239m6.985s
# sys     20m9.822s
#
# real    12m34.191s
# user    258m20.514s
# sys     21m45.155s
