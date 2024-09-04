import csv
import locale


def tr(
    csv_file,
    target_key,
    langcode=locale.getlocale()[0].split("_")[0],
) -> str:
    f = open(csv_file, newline="")
    locale_csv = csv.DictReader(f=f, delimiter=",")
    for item in locale_csv:
        if item["stringname"] == target_key:
            try:
                if item[langcode] == "":
                    f.close()
                    return item["en"]
                else:
                    f.close()
                    return item[langcode]
            except:
                f.close()
                return item["en"]
