from bs4 import BeautifulSoup
import re
import itertools
import sys
import datetime
import logging
import argparse

logging.basicConfig(
    format='%(asctime)s [%(filename)s::%(funcName)s] %(levelname)s %(message)s',
    level=logging.DEBUG
)


class CucumberFeaturesDurationParser(object):
    """
    One parser to group features based on the threshold
    """

    def __init__(self, html, threshold):
        try:
            self.soup = BeautifulSoup(open(html), features="lxml")
            self.threshold = threshold
        except Exception:
            logging.info(
                'Failed to open the cucumber htmnl report:{}'.format())

    def __calculate_time(self, duration):
        '''
        return duration_seconds: int
        '''
        time_list = duration.split(' ')
        real_time = 0
        for time in time_list:
            if time.find('m') > 0 and time.find('ms') < 0:
                real_time += int(time.strip('m')) * 60
            if time.find('s') > 0 and time.find('ms') < 0:
                real_time += int(time.strip('s'))
        return real_time

    def __get_features_list_from_soap(self):
        '''
        return []: features_list
        '''
        logging.info('Get features list from the soap')
        features_list = []
        for feature in self.soup.find_all('a', href=re.compile('report-feature*')):
            features_list.append(feature.text)
        return features_list

    def __get_time_list_from_soap(self):
        '''
        return []: time_list
        '''
        logging.info('Get time list from the soap')
        time_list = []
        for duration in self.soup.find_all('td', {'class': 'duration'}):
            time = self.__calculate_time(duration.text)
            time_list.append(time)
        return time_list

    def __get_whole_duration(self, feature_time_map):
        '''
        return int: the duration of the features dictionary
        '''
        total_duration = 0
        logging.info('Begin: get the duration of the features')
        for feature, time in feature_time_map.items():
            total_duration += time
        logging.info(
            'Complete: the total duration is {}'.format(total_duration))
        return total_duration

    def get_features_durations_map(self):
        '''
        return {}: features_durations_map
        '''
        logging.info('Begin: get the features and durations map')
        features_time_map = {}
        try:
            features_list = self.__get_features_list_from_soap()
            time_list = self.__get_time_list_from_soap()
            features_time_map = dict(zip(features_list, time_list))
            logging.info('Complete: get the features and durations map')
            logging.info(features_time_map)
        except Exception:
            logging.info('Fail to get features and durations map!')

        return features_time_map

    def spilt_features_to_groups_by_threshold(self, feature_time_map, time_threshold):
        '''
        return []: features groups list
        '''
        logging.info('Begin: split features {} to groups by the threshold {}'.format(
            feature_time_map, time_threshold))
        features_groups_list = []
        total_time = 0
        begin_index = 0
        end_index = 0
        for feature, time in feature_time_map.items():
            if total_time < int(time_threshold):
                total_time += time
            else:
                end_index = list(feature_time_map.keys()).index(feature)
                feature_time_map_featuers = list(feature_time_map.keys())[
                    begin_index:end_index]
                feature_time_map_time = list(feature_time_map.values())[
                    begin_index:end_index]
                features_groups_list.append(
                    dict(zip(feature_time_map_featuers, feature_time_map_time)))
                begin_index = end_index
                total_time = 0

        ungrouped_feature_time_map_features = list(
            feature_time_map.keys())[begin_index:]
        ungrouped_feature_time_map_time = list(
            feature_time_map.values())[begin_index:]
        features_groups_list.append(
            dict(zip(ungrouped_feature_time_map_features, ungrouped_feature_time_map_time)))
        logging.info('Complete: the grouped features are ready: \n{}'.format(
            features_groups_list))
        return features_groups_list

    def format_features_groups(self, features_groups_list):
        '''
        return {}: {'-n feature..': duration, ...}
        '''
        logging.info(
            'Begin: format the grouped features and durations with cucumber ops "-n"')
        formmated_features_groups = {}
        for features_group in features_groups_list:
            features_string = ''
            total_time = 0
            for feature, time in features_group.items():
                features_string += " -n '{}'".format(feature)
                total_time += time
            formmated_features_groups[features_string] = total_time

        logging.info('Complete: format the grouped features as below:\n{}'.format(
            formmated_features_groups))
        return formmated_features_groups

    def confirm_the_grouped_result(self, formmated_features_groups, feature_time_map):
        '''
        return 0/1
        '''
        total_time = 0
        logging.info(
            'Begin: compare the duration the new grouped features with the original features')
        if self.__get_whole_duration(formmated_features_groups) == self.__get_whole_duration(feature_time_map):
            logging.info(
                'Complete: features are grouped successfully, Cheers!')
            return 0
        else:
            logging.info('Complete: features are failed to be grouped, Sorry!')
            return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cucumber-html-report',
                        help='The cucumber html report path')
    parser.add_argument(
        '--threshold', help='The threshold of the duration of each feature group')
    args = parser.parse_args()
    cucumber_html_report = args.cucumber_html_report
    threshold = args.threshold
    cucumber_report_duration_parser = CucumberFeaturesDurationParser(
        cucumber_html_report, threshold)
    feature_time_map = cucumber_report_duration_parser.get_features_durations_map()
    features_groups_list = cucumber_report_duration_parser.spilt_features_to_groups_by_threshold(
        feature_time_map, threshold)
    formmated_features_groups = cucumber_report_duration_parser.format_features_groups(
        features_groups_list)
    cucumber_report_duration_parser.confirm_the_grouped_result(
        formmated_features_groups, feature_time_map)
