import json
import pandas as pd

from string import ascii_lowercase as alc

from TableProcessing.WordMatching import WordMatching


class SizeChartProcessing:
    ENGLISH = "en"
    MEASUREMENT_KEYWORDS = ["measurement", "measure", "name"]
    TOLERANCE_KEYWORDS = ["tolerance", "tol"]
    SIZE_REGEX_PATTERN = {
        "XS_PATTERN": ".*xs.*",
        "XL_PATTERN": ".*xl.*",
        "SML_PATTERN": "^[sml]$",
        "DIGIT_PATTERN": "^\d{0,2}$",
    }

    def __init__(self, file_path="", full_output_path="", language="en", unit_system="metrics"):
        self.language = language
        self.units = unit_system

        self.file_path = file_path
        self.full_output_path = full_output_path

        self.word_matching = WordMatching()
        self.reset_values()

    def reset_values(self):
        self.df = None
        self.skiprows = 0

        self.size_column_headers_indices = None
        self.size_option_list = None
        self.measurement_column_header_index = None

    def run(self):
        self.df = self.load_table(self.file_path)

        # size/option headers
        self.find_size_headers()

        # measurement name list if "Measure" header exists
        measurement_column_header_index = self.find_measurement_column_header()

        if not measurement_column_header_index:
            tolerance_column_header_index = self.find_tolerance_column_header()

            if tolerance_column_header_index:
                # if the tolerance column is located left to the size columns, we assume the measurement column will be one column to the left of the tolerance column
                if tolerance_column_header_index == self.size_column_headers_indices[0] - 1:
                    measurement_column_header_index = tolerance_column_header_index - 1

                # else if the tolerance column is at the end of the table, we assume that the measurement column will be one column to the left of the first size column
                # else, if the tolerance column is not present, we also assume that the measurement column will be one column to the left of the first size column
                else:
                    measurement_column_header_index = self.size_column_headers_indices[0] - 1
            # if the tolerance column is not found and the measurement column is also not found, we assume the measurement column is just to the left of the first size column
            else:
                measurement_column_header_index = self.size_column_headers_indices[0] - 1

        measurement_column__header_name = self.df.columns[measurement_column_header_index]
        measurement_name_list = self.get_measurement_list_from_column_header(measurement_column__header_name)
        amount_of_measurements = len(measurement_name_list)

        measurement_values, skipped_row_indices = self.extract_measurement_data_row_per_row(amount_of_measurements,
                                                                                            self.size_column_headers_indices)
        filtered_measurement_name_list = [item for index, item in enumerate(measurement_name_list) if
                                          index not in skipped_row_indices]

        const_dimension_measurement_indices = self.extract_constant_value_rows(measurement_values)
        const_dimension_measurement_names, const_dimension_size_options, filtered_out_indices = self.extract_const_dim_common_substrings(
            filtered_measurement_name_list, const_dimension_measurement_indices)

        filtered_measurement_name_list = [item for index, item in enumerate(filtered_measurement_name_list) if
                                          index not in filtered_out_indices]

        measurement_with_values_dict = self.setup_measurements_dictionary(filtered_measurement_name_list,
                                                                          measurement_values,
                                                                          const_dimension_measurement_indices,
                                                                          const_dimension_size_options,
                                                                          const_dimension_measurement_names)

        json_export_data = self.construct_export_format(self.size_option_list, measurement_with_values_dict)

        self.export_json(json_export_data)
        self.reset_values()

    def load_table(self, file_path, skiprows=None):
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path, skiprows=skiprows)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            self.df = pd.read_excel(file_path, skiprows=skiprows)
        else:
            raise ValueError("Unsupported file format")
        return self.df

    def find_size_headers(self):
        self.size_column_headers_indices, self.size_option_list = self.find_matching_size_column_headers()
        if len(self.size_column_headers_indices) == 0:
            self.skiprows += 1
            self.df = self.load_table(self.file_path, skiprows=self.skiprows)
            self.find_size_headers()

    def find_matching_size_column_headers(self):
        size_column_headers = []
        size_option_list = []
        for index, header in enumerate(self.df.columns):
            header_string = str(header)
            lowercase_header = header_string.lower()
            is_size_matched = self.word_matching.is_regex_matches(lowercase_header,
                                                                  patterns=self.SIZE_REGEX_PATTERN)
            if is_size_matched:
                size_column_headers.append(index)
                size_option_list.append(header_string)
        return size_column_headers, size_option_list

    def find_measurement_column_header(self, iteration=0):
        measurement_column_header_index = None
        # TODO: This can potentially be an issue
        if iteration < 10:
            if iteration == 0:
                new_column_list = self.df.columns.tolist()
            else:
                new_column_list = self.df.iloc[iteration - 1].tolist()
            string_column_headers, translated_string_column_headers = self.find_matching_string_headers(new_column_list)
            measurement = self.word_matching.find_most_similar_word_from_list(translated_string_column_headers,
                                                                              self.MEASUREMENT_KEYWORDS)
            if measurement is None:
                self.find_measurement_column_header(iteration=iteration + 1)
            else:
                self.df = self.load_table(self.file_path, skiprows=iteration + self.skiprows)
                original_measurement = string_column_headers[translated_string_column_headers.index(measurement)]
                measurement_column_header_index = new_column_list.index(original_measurement)
        return measurement_column_header_index

    def find_tolerance_column_header(self, iteration=0):
        tolerance_column_header_index = None
        if iteration < 2:
            if iteration == 0:
                new_column_list = self.df.columns.tolist()
            else:
                new_column_list = self.df.iloc[iteration - 1].tolist()
            string_column_headers, translated_string_column_headers = self.find_matching_string_headers(new_column_list)
            tolerance = self.word_matching.find_most_similar_word_from_list(translated_string_column_headers,
                                                                            self.TOLERANCE_KEYWORDS)
            if tolerance is None:
                self.find_tolerance_column_header(iteration=iteration + 1)
            else:
                self.df = self.load_table(self.file_path, skiprows=iteration + self.skiprows)
                original_tolerance = string_column_headers[translated_string_column_headers.index(tolerance)]
                tolerance_column_header_index = new_column_list.index(original_tolerance)
        return tolerance_column_header_index

    def find_matching_string_headers(self, header_list):
        string_column_headers = []
        translated_string_column_headers = []
        for index, header in enumerate(header_list):
            if isinstance(header, str):
                lowercase_header = header.lower()
                is_alpha_matched = self.word_matching.is_alpha_match(lowercase_header)
                if is_alpha_matched:
                    translated_header = header
                    if self.language != self.ENGLISH:
                        translated_header = self.word_matching.translate_words(header, self.language, self.ENGLISH)
                    string_column_headers.append(header)
                    translated_string_column_headers.append(translated_header)
        return string_column_headers, translated_string_column_headers

    def get_measurement_list_from_column_header(self, column_header):
        column_values = self.df[column_header]
        value_list = column_values.tolist()
        return value_list

    def get_measurement_list_length_from_column_index(self, column_index):
        column_values = self.df.iloc[:, column_index]
        value_list = column_values.tolist()
        return len(value_list)

    def extract_measurement_data_row_per_row(self, amount_of_measurements, size_column_headers_indices):
        row_per_row_data_list = []
        skipped_row_indices = []
        first_size_index, last_size_index = size_column_headers_indices[0], size_column_headers_indices[-1] + 1
        for measurement_iter in range(amount_of_measurements):
            subsection = self.df.iloc[measurement_iter, first_size_index:last_size_index]
            if subsection.isna().any() or (subsection.apply(lambda x: str(x).strip() == '')).any():
                skipped_row_indices.append(measurement_iter)
            else:
                row_per_row_data_list.append(subsection.values.tolist())
        return row_per_row_data_list, skipped_row_indices

    def extract_constant_value_rows(self, measurement_values):
        constant_indices = []
        for measurement_index, measurement_value in enumerate(measurement_values):
            if all(item == measurement_value[0] for item in measurement_value):
                constant_indices.append(measurement_index)
        return constant_indices

    def extract_const_dim_common_substrings(self, measurement_name_list, measurement_indices):
        # Filter the measurement_name_list to include only elements at the specified indices
        constant_measurement_name_list = [measurement_name_list[index] for index in measurement_indices]

        most_common_substring = find_most_common_substring(constant_measurement_name_list)

        # Filter out strings that do not start with the most common substring
        const_dimension_measurement_names = {}
        filtered_list = []
        deactivate_const_size_option_flag = False
        const_dimension_size_options = []
        for substring in most_common_substring:
            substring_filtered_indices_list = []
            substring_filtered_list = []
            for index, s in enumerate(constant_measurement_name_list):
                if substring in s:
                    substring_filtered_indices_list.append(measurement_name_list.index(s))
                    substring_filtered_list.append(s)
            filtered_list += substring_filtered_list

            const_dimension_measurement_names.update({substring: substring_filtered_indices_list})

            if not deactivate_const_size_option_flag:
                size_option_difference = [s[len(substring):].strip() for s in substring_filtered_list]
                if len(const_dimension_size_options) == 0:
                    const_dimension_size_options = size_option_difference
                elif size_option_difference != const_dimension_size_options:
                    const_dimension_size_options = [alc[i] for i in range(len(const_dimension_size_options))]
                    deactivate_const_size_option_flag = True

        filtered_out_indices = [measurement_indices[i] for i, s in enumerate(constant_measurement_name_list) if
                                s not in filtered_list]

        return const_dimension_measurement_names, const_dimension_size_options, filtered_out_indices

    def setup_measurements_dictionary(self, measurement_name_list, measurement_values,
                                      const_dimension_measurement_indices, const_dimension_measurement_sizes,
                                      const_dimension_measurement_names):
        measurement_name_dict = {}
        for index, measurement_name in enumerate(measurement_name_list):
            self.setup_measurements(measurement_name_dict, measurement_name, measurement_values[index], index,
                                    const_dimension_measurement_indices, const_dimension_measurement_sizes,
                                    const_dimension_measurement_names)
        return measurement_name_dict

    def setup_measurements(self, measurement_name_dict, measurement_name, measurement_values, index,
                           const_dimension_measurement_indices, const_dimension_measurement_sizes,
                           const_dimension_measurement_names):
        # dimension 2 const
        if index in const_dimension_measurement_indices:
            self.setup_const_dimensional_measurements(index, measurement_name_dict, measurement_values, const_dimension_measurement_names, const_dimension_measurement_sizes)

        # dimension 1
        elif measurement_name not in measurement_name_dict:
            measurement_name_dict[measurement_name] = {"cross": False, "dim1": measurement_values}

        # dimension 2 cross
        else:
            self.setup_cross_dimensional_measurements(measurement_name_dict, measurement_name, measurement_values)

    def setup_const_dimensional_measurements(self, index, measurement_name_dict, measurement_values, const_dimension_measurement_names, const_dimension_measurement_sizes):
        const_dim_measurement_name = ""
        for key in const_dimension_measurement_names:
            if index in const_dimension_measurement_names[key]:
                const_dim_measurement_name = key
                break
        if const_dim_measurement_name != "":
            if const_dim_measurement_name not in measurement_name_dict:
                measurement_name_dict[const_dim_measurement_name] = {"cross": False, "dim2": {
                    const_dimension_measurement_sizes[0]: measurement_values[0]}}
            else:
                dim2_dict_length = len(measurement_name_dict[const_dim_measurement_name].get("dim2", []))
                measurement_name_dict[const_dim_measurement_name]["dim2"].update(
                    {const_dimension_measurement_sizes[dim2_dict_length]: measurement_values[0]})

    def setup_cross_dimensional_measurements(self, measurement_name_dict, measurement_name, measurement_values):
        cross_dict_length = len(measurement_name_dict[measurement_name].get("dim2", []))
        cross_value_dict = {alc[cross_dict_length]: measurement_values}
        measurement_name_dict[measurement_name]["cross"] = True
        if "dim2" not in measurement_name_dict[measurement_name]:
            measurement_name_dict[measurement_name].update({"dim2": cross_value_dict})
        else:
            measurement_name_dict[measurement_name]["dim2"].update(cross_value_dict)

    def construct_export_format(self, size_list, measurement_name_dict):
        metadata_dict = {
            "units": self.units,
            "options": size_list,
            "measurements": measurement_name_dict
        }
        return metadata_dict

    def export_json(self, export_content):
        with open(self.full_output_path, 'w') as fp:
            json.dump(export_content, fp, indent=4)


def find_most_common_substring(list_of_strings):
    if not list_of_strings:
        return []

    longest_substring = []
    longest_substring_length = 0

    # Compare every pair of strings in the list
    for i in range(len(list_of_strings)):
        longest_common_substring_frequency = {}
        for j in range(i + 1, len(list_of_strings)):
            longest_common_substring = find_max_common_substring(list_of_strings[i], list_of_strings[j])

            # If an LCS is found, update its frequency in the dictionary
            if longest_common_substring:
                if longest_common_substring in longest_common_substring_frequency:
                    longest_common_substring_frequency[longest_common_substring] += 1
                else:
                    longest_common_substring_frequency[longest_common_substring] = 1
        # Filter list to only store the highest matching values
        for substring in longest_common_substring_frequency:
            lcs_length = longest_common_substring_frequency[substring]
            if lcs_length > longest_substring_length:
                longest_substring = [substring]
                longest_substring_length = lcs_length
            elif lcs_length == longest_substring_length:
                longest_substring.append(substring)

    return longest_substring


def find_max_common_substring(s1, s2):
    m = len(s1)
    n = len(s2)

    res = 0  # This will store the length of the longest common substring
    end_index_in_s1 = -1  # This will store the ending index in s1 where the LCS ends

    # Create a table to store lengths of longest common suffixes for substrings.
    # The first row and first column entries have no logical meaning, they are used only for simplicity of the program.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
                # Update the result if we find a longer common substring
                if dp[i + 1][j + 1] > res:
                    res = dp[i + 1][j + 1]
                    end_index_in_s1 = i

    # If no common substring is found, return an empty string
    if end_index_in_s1 == -1 or res < 3:
        return ""

    # Extract the longest common substring from s1 using the stored index
    lcs = s1[end_index_in_s1 - res + 1: end_index_in_s1 + 1]
    return lcs


if __name__ == "__main__":
    # table_file_path = "../GroundTruth/BRITISH AIRWAYS - BAOLJ2 - Ladies Suit Jacket in Oxford Blue (1).csv"
    table_file_path = "../GroundTruth/BRITISH AIRWAYS - BAOLJ2 - Ladies Suit Jacket in Oxford Blue (1)_SML_PATTERN.csv"
    table_language = "en"
    size_chart_processing = SizeChartProcessing(table_file_path, table_language)
    size_chart_processing.run()
