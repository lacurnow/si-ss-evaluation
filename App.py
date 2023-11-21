from SpecialIssueEvaluation import SpecialIssueEvaluator
from datetime import datetime
import csv

class App:
    def __init__(self) -> None:
        self.specialIssueEvaluator = SpecialIssueEvaluator()

    def start(self, source_of_truth_files: str, bool_result_eids_file: str, vector_result_eids_file: str) -> None:
        dt = datetime.now()
        dt_string = dt.isoformat()

        # Parse eid data from files
        special_issue_dict = \
            self.specialIssueEvaluator.get_data_from_results(source_of_truth_files)

        bool_results_dict = self.specialIssueEvaluator.get_data_from_long_results(bool_result_eids_file)
        vector_results_dict = self.specialIssueEvaluator.get_data_from_long_results(vector_result_eids_file)

        # bool_results_dict = self.specialIssueEvaluator.get_data_from_results(bool_result_eids_file)
        # vector_results_dict = self.specialIssueEvaluator.get_data_from_results(vector_result_eids_file)

        # For each key in special issue dict, we want to compute similarity of eids
        fieldnames = ["SI_ID", "boolean_recall", "vector_recall", "boolean_similarity_score",
                      "vector_similarity_score", "boolean_jaccard_similarity_score", "vector_jaccard_similarity_score"]

        with open(f"similarity_results_{dt_string}.csv", "a", newline="", encoding='utf-8-sig') as results_file:
            writer = csv.DictWriter(results_file, fieldnames)
            writer.writeheader()

            for special_issue_id in special_issue_dict:
                special_issue_eids = special_issue_dict.get(special_issue_id)
                sim_data = {}
                bool_result_eids = bool_results_dict.get(special_issue_id)
                vector_result_eids = vector_results_dict.get(special_issue_id)

                bool_recall = self.specialIssueEvaluator.compute_recall(special_issue_eids, bool_result_eids)
                vector_recall = self.specialIssueEvaluator.compute_recall(special_issue_eids, vector_result_eids)

                bool_sim = self.specialIssueEvaluator.compute_similarity(special_issue_eids, bool_result_eids)
                vector_sim = self.specialIssueEvaluator.compute_similarity(special_issue_eids, vector_result_eids)

                bool_jaccard = self.specialIssueEvaluator.jaccard_similarity(special_issue_eids, bool_result_eids)
                vector_jaccard = self.specialIssueEvaluator.jaccard_similarity(special_issue_eids, vector_result_eids)

                sim_data["SI_ID"] = special_issue_id
                sim_data["boolean_recall"] = bool_recall
                sim_data["vector_recall"] = vector_recall
                sim_data["boolean_similarity_score"] = bool_sim
                sim_data["vector_similarity_score"] = vector_sim
                sim_data["boolean_jaccard_similarity_score"] = bool_jaccard
                sim_data["vector_jaccard_similarity_score"] = vector_jaccard

                writer.writerow(sim_data)

        self.specialIssueEvaluator.calculate_similarity_metrics(f"similarity_results_{dt_string}.csv", dt_string)


######################################################################################
# Test
######################################################################################

if __name__ == "__main__":
    source_of_truth_files = "sot_eval_SIs_short_eid_list.csv"
    bool_result_file = "sot_eval_SIs_short_eid_list.csv"
    vector_result_file = "eval_tester_placeholder_vector_boolean.csv"

    App().start(source_of_truth_files, bool_result_file, vector_result_file)


