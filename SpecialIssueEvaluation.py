import csv
import os
import difflib
import sys
import pandas as pd
from datetime import datetime

class SpecialIssueEvaluator:

    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    def get_data_for_special_issues(self, file_path):
        special_issues = {}
        with os.scandir(file_path) as it:
            for entry in it:
                if entry.name.endswith(".csv") and entry.is_file():
                    special_issue_id = entry.name.replace('.csv', '')
                    data = {}
                    data['EID'] = self._get_column_data(entry, "EID_list")

                    special_issues[special_issue_id] = data

        return special_issues

    def get_data_from_results(self, file_path):
        results_si_to_eid = {}

        with open(file_path, "r",  newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                results_si_to_eid[row["SI_ID"]] = row["EID_list"]

        return results_si_to_eid

    def _get_column_data(self, csv_file, column_name):
        data = []
        with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            if column_name not in reader.fieldnames:
                print(f"Error: Column '{column_name}' not found in the CSV file.")
                return None

            for row in reader:
                data.append(row[column_name])

        return data

    def compute_recall(self, gt, pred):
        gt_set = set(gt)
        pred_set = set(pred)
        intersection = gt_set.intersection(pred_set)
        recall = len(intersection) / float(len(gt_set))

        return recall

    def compute_similarity(self, list1, list2):
        similarities = difflib.SequenceMatcher(None, list1, list2)
        ratio = similarities.ratio()
        return ratio

    def jaccard_similarity(self, list1, list2):
        intersection = len(set(list1) & set(list2))
        union = len(set(list1) | set(list2))

        similarity = intersection / union
        return similarity

    def calculate_similarity_metrics(self, similarity_results_file: str, datetime: str):
        df = pd.read_csv(similarity_results_file)
        del df['SI_ID']

        mean_scores = df.mean()
        standard_deviation = df.std()

        stats_df = pd.DataFrame(mean_scores, columns=["mean_scores"])
        stats_df["standard_deviation"] = standard_deviation

        stats_df.index.names = ["similarity_metric"]

        stats_df.to_csv(f"metrics_{datetime}")


######################################################################################
# Test
######################################################################################

if __name__ == "__main__":
    datetime = datetime.now().isoformat()

    file = "/Users/curnowl/Documents/test.csv"
    results_file = "/Users/curnowl/Developer/scopus-search-evaluaton/similarity_results_2023-11-20T16:27:05.593804.csv"

    evaluator = SpecialIssueEvaluator()
    evaluator.calculate_similarity_metrics(results_file, datetime)
