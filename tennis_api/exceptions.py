from rest_framework.exceptions import APIException


class IncompleteProfile(APIException):
    status_code = 400
    default_detail = 'Incomplete profile.'
    default_code = 'incomplete_profile'


class LeagueAlreadyJoined(APIException):
    status_code = 400
    default_detail = 'League already joined'
    default_code = 'already_joined_league'


class LeagueDoesntJoined(APIException):
    status_code = 400
    default_detail = 'League does not joined'
    default_code = 'does_not_joined_league'


class LeagueNotOpened(APIException):
    status_code = 400
    default_detail = 'League is not OPENED'
    default_code = 'not_opened_league'


class NotEnoughPlayersToStartLeague(APIException):
    status_code = 400
    default_detail = 'There is not enough players to start the league'
    default_code = 'not_enough_players'


class WrongLeagueStatusToStart(APIException):
    status_code = 400
    default_detail = 'League can be started only if its status is OPENED'
    default_code = 'not_opened_league_to_start'


class ChangeLeagueStatus(APIException):
    status_code = 400
    default_detail = 'Unable to change league status.'
    default_code = 'change_league_status_error'


class CreateScheduleError(APIException):
    status_code = 400
    default_detail = 'Unable to create a competition schedule.'
    default_code = 'create_schedule_error'
