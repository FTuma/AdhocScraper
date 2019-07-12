NR == 1 {
        for (i = 1; i <= NF; i++) headers[i] = $i;
        next
}

{
        # find maximum value
        max = $2
        for (i = 4; i <= NF; i += 2) if ($i > max) max = $i;
        # print row id
        printf "%s", $1
        # print all lc# column values (assuming the column 
        # after the max value sno# column)
        sep = OFS
        for (i = 2; i <= NF; i += 2) {
                if ($i == max) {
                        printf "%s%s", sep, $(i + 1);
                        sep = ","
                }
        }
        # print all column headers of the max value columns
        sep = OFS
        for (i = 2; i <= NF; i += 2) {
                if ($i == max) {
                        printf "%s%s", sep, headers[i];
                        sep = ","
                }
        }
        printf "\n"
}
