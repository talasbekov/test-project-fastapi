from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer


router = APIRouter(
    prefix="/actions",
    tags=["Action"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get('')
async def get_all_actions():
    return [
    {
        'action_name': 'Добавление медали',
        'action_nameKZ': 'Қосуға арналған медаль',
        'action_type': 'add_badge',
        'children': [
            {
                'alias_name': 'Медаль для добавления',
                'alias_nameKZ': 'Қосуға арналған медаль',
                'tagname': 'badge_name',
                'data_taken': 'dropdown',
                'field_name': 'badges',
            },
        ],
        'properties': {
            'badge_name': {
                'alias_name': 'Медаль для добавления',
                'alias_nameKZ': 'Қосуға арналған медаль',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'badges',
            },
        },
        'actions': {
            'args': [
                {
                    'add_badge': {
                        'badge': {
                            'tagname': 'badge_name',
                            'alias_name': 'Медаль для добавления',
                            'alias_nameKZ': 'Қосуға арналған медаль',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Лишение медали',
        'action_nameKZ': 'Медальдан айыру',
        'action_type': 'delete_badge',
        'children': [
            {
                'alias_name': 'Медаль для лишения',
                'alias_nameKZ': 'Медальдан айыру үшін',
                'tagname': 'badge_name',
                'data_taken': 'dropdown',
                'field_name': 'badges',
            },
        ],
        'properties': {
            'badge_name': {
                'alias_name': 'Медаль для лишения',
                'alias_nameKZ': 'Медальдан айыру үшін',
                'type': 'delete',
                'data_taken': 'dropdown',
                'field_name': 'badges',
            },
        },
        'actions': {
            'args': [
                {
                    'delete_badge': {
                        'badge': {
                            'tagname': 'badge_name',
                            'alias_name': 'Медаль для лишения',
                            'alias_nameKZ': 'Медальдан айыру үшін',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Выход в отпуск',
        'action_nameKZ': 'Демалысқа шығу',
        'action_type': 'grant_leave',
        'children': [
            {
                'alias_name': 'Выход в отпуск',
                'alias_nameKZ': 'Демалысқа шығу',
                'tagname': 'status',
                'data_taken': 'dropdown',
                'field_name': 'status_leave',
            },
            {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'tagname': 'date_from',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'tagname': 'date_to',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        ],
        'properties': {
            'status': {
                'alias_name': 'Выход в отпуск',
                'alias_nameKZ': 'Демалысқа шығу',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'status_leave',
            },
            'date_from': {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            'date_to': {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        },
        'actions': {
            'args': [
                {
                    'grant_leave': {
                        'status': {
                            'tagname': 'status',
                            'alias_name': 'Выход в отпуск',
                            'alias_nameKZ': 'Демалысқа шығу',
                        },
                        'date_from': {
                            'tagname': 'date_from',
                            'alias_name': 'Дата начала',
                            'alias_nameKZ': 'Басталу күні',
                        },
                        'date_to': {
                            'tagname': 'date_to',
                            'alias_name': 'Дата конца',
                            'alias_nameKZ': 'Аяқталу күні',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Отзыв с отпуска',
        'action_nameKZ': 'Демалыс туралы пікір',
        'action_type': 'stop_leave',
        'children': [
            {
                'alias_name': 'Причина',
                'alias_nameKZ': 'Себеп',
                'tagname': 'reason',
                'data_taken': 'manual',
                'data_type': 'string',
            },
        ],
        'properties': {
            'reason': {
                'alias_name': 'Причина',
                'alias_nameKZ': 'Себеп',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'string',
            }
        },
        'actions': {
            'args': [
                {
                    'stop_leave': {
                        'reason': {
                            'tagname': 'reason',
                            'alias_name': 'Причина',
                            'alias_nameKZ': 'Себеп',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Контракт',
        'action_nameKZ': 'Контракт',
        'action_type': 'renew_contract',
        'children': [
            {
                'alias_name': 'Контракт',
                'alias_nameKZ': 'Контракт',
                'tagname': 'contract_type',
                'data_taken': 'dropdown',
                'field_name': 'contracts',
            },
        ],
        'properties': {
            'contract_type': {
                'alias_name': 'Контракт',
                'alias_nameKZ': 'Контракт',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'contracts',
            },
        },
        'actions': {
            'args': [
                {
                    'renew_contract': {
                        'contract': {
                            'tagname': 'contract_type',
                            'alias_name': 'Контракт',
                            'alias_nameKZ': 'Контракт',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Добавление дисциплинарного взыскания',
        'action_nameKZ': 'Тәртіптік жазаны қосу',
        'action_type': 'add_penalty',
        'children': [
            {
                'alias_name': 'Строгость',
                'alias_nameKZ': 'Қатаңдық',
                'tagname': 'penalty',
                'data_taken': 'dropdown',
                'field_name': 'penalties',
            },
            {
                'alias_name': 'Причина',
                'alias_nameKZ': 'Себебi',
                'tagname': 'reason',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'string',
            },
        ],
        'properties': {
            'penalty': {
                'alias_name': 'Строгость',
                'alias_nameKZ': 'Қатаңдық',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'penalties',
            },
            'reason': {
                'alias_name': 'Причина',
                'alias_nameKZ': 'Себебi',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'string',
            },
        },
        'actions': {
            'args': [
                {
                    'add_penalty': {
                        'penalty': {
                            'tagname': 'penalty',
                            'alias_name': 'Строгость',
                            'alias_nameKZ': 'Қатаңдық',
                        },
                        'reason': {
                            'tagname': 'reason',
                            'alias_name': 'Причина',
                            'alias_nameKZ': 'Себебi',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Снятие дисциплинарного взыскания',
        'action_nameKZ': 'Тәртіптік жазаны алып тастау',
        'action_type': 'delete_penalty',
        'children': [
            {
                'alias_name': 'Взыскание для снятия',
                'alias_nameKZ': 'Алып тастауға арналған жаза',
                'tagname': 'penalty',
                'data_taken': 'dropdown',
                'field_name': 'penalties',
            },
        ],
        'properties': {
            'penalty': {
                'alias_name': 'Взыскание для снятия',
                'alias_nameKZ': 'Алып тастауға арналған жаза',
                'type': 'delete',
                'data_taken': 'dropdown',
                'field_name': 'penalties',
            },
        },
        'actions': {
            'args': [
                {
                    'delete_penalty': {
                        'penalty': {
                            'tagname': 'penalty',
                            'alias_name': 'Взыскание для снятия',
                            'alias_nameKZ': 'Алып тастауға арналған жаза',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Добавление черного берета',
        'action_nameKZ': 'Қара берет қосу',
        'action_type': 'add_black_beret',
        'children': [],
        'properties': {},
        'actions': {
            'args': [
                {
                    'add_black_beret': {},
                },
            ],
        },
    },
    {
        'action_name': 'Лишение черного берета',
        'action_nameKZ': 'Қара береттен айыру',
        'action_type': 'delete_black_beret',
        'children': [],
        'properties': {},
        'actions': {
            'args': [
                {
                    'delete_black_beret': {},
                },
            ],
        },
    },
    {
        'action_name': 'Временная смена статуса',
        'action_nameKZ': 'Уақытша мәртебені өзгерту',
        'action_type': 'temporary_status_change',
        'children': [
            {
                'alias_name': 'Временный статус',
                'alias_nameKZ': 'Уақытша мәртебе',
                'tagname': 'status',
                'data_taken': 'dropdown',
                'field_name': 'statuses',
            },
            {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'tagname': 'date_from',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'tagname': 'date_to',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        ],
        'properties': {
            'status': {
                'alias_name': 'Временный статус',
                'alias_nameKZ': 'Уақытша мәртебе',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'statuses',
            },
            'date_from': {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            'date_to': {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        },
        'actions': {
            'args': [
                {
                    'temporary_status_change': {
                        'status': {
                            'tagname': 'status',
                            'alias_name': 'Временный статус',
                            'alias_nameKZ': 'Уақытша мәртебе',
                        },
                        'date_from': {
                            'tagname': 'date_from',
                            'alias_name': 'Дата начала',
                            'alias_nameKZ': 'Басталу күні',
                        },
                        'date_to': {
                            'tagname': 'date_to',
                            'alias_name': 'Дата конца',
                            'alias_nameKZ': 'Аяқталу күні',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Добавление прикомандирования',
        'action_nameKZ': 'Іссапарды қосу',
        'action_type': 'add_secondment',
        'children': [
            {
                'alias_name': 'Департамент для прикомандирования',
                'alias_nameKZ': 'Іссапарды қосу департаменті',
                'tagname': 'status',
                'data_taken': 'dropdown',
                'field_name': 'secondments',
            },
            {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'tagname': 'date_from',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'tagname': 'date_to',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        ],
        'properties': {
            'secondment': {
                'alias_name': 'Департамент для прикомандирования',
                'alias_nameKZ': 'Іссапарды қосу департаменті',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'secondments',
            },
            'date_from': {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            'date_to': {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        },
        'actions': {
            'args': [
                {
                    'add_secondment': {
                        'secondment': {
                            'tagname': 'secondment',
                            'alias_name': 'Департамент для прикомандирования',
                            'alias_nameKZ': 'Іссапарды қосу департаменті',
                        },
                        'date_from': {
                            'tagname': 'date_from',
                            'alias_name': 'Дата начала',
                            'alias_nameKZ': 'Басталу күні',
                        },
                        'date_to': {
                            'tagname': 'date_to',
                            'alias_name': 'Дата конца',
                            'alias_nameKZ': 'Аяқталу күні',
                        },
                    },
                },
            ],
        },
    },
    # {
    #     'action_name': "Добавление откомандирования",
    #     'action_nameKZ': "Іссапарды қосу",
    #     'action_type': 'add_secondment_to_state_body',
    #     'children': [
    #         {
    #             'alias_name': 'Гос. орган для откомандирования',
    #             'alias_nameKZ': 'Іссапарды қосу үшін мемлекеттік орган',
    #             'tagname': 'state_body',
    #             'data_taken': 'dropdown',
    #             'field_name': 'state_body',
    #         },
    #         {
    #             'alias_name': 'Дата начала',
    #             'alias_nameKZ': 'Басталу күні',
    #             'tagname': 'date_from',
    #             'data_taken': 'manual',
    #             'data_type': 'date',
    #         },
    #         {
    #             'alias_name': 'Дата конца',
    #             'alias_nameKZ': 'Аяқталу күні',
    #             'tagname': 'date_to',
    #             'data_taken': 'manual',
    #             'data_type': 'date',
    #         }],
    #     'properties': {
    #         'state_body': {
    #             'alias_name': 'Гос. орган для откомандирования',
    #             'alias_nameKZ': 'Іссапарды қосу үшін мемлекеттік орган',
    #             'type': 'write',
    #             'data_taken': 'dropdown',
    #             'field_name': 'state_body',
    #         },
    #         'date_from': {
    #             'alias_name': 'Дата начала',
    #             'alias_nameKZ': 'Басталу күні',
    #             'type': 'read',
    #             'data_taken': 'manual',
    #             'data_type': 'date',
    #         },
    #         'date_to': {
    #             'alias_name': 'Дата конца',
    #             'alias_nameKZ': 'Аяқталу күні',
    #             'type': 'read',
    #             'data_taken': 'manual',
    #             'data_type': 'date',
    #         },
    #     },
    #     'actions': {
    #         'args': [
    #             {
    #                 'add_secondment_to_state_body': {
    #                     'secondment': {
    #                         'tagname': 'state_body',
    #                         'alias_name': 'Гос. орган для откомандирования',
    #                         'alias_nameKZ': 'Іссапарды қосу үшін мемлекеттік орган',
    #                     },
    #                     'date_from': {
    #                         'tagname': 'date_from',
    #                         'alias_name': 'Дата начала',
    #                         'alias_nameKZ': 'Басталу күні',
    #                     },
    #                     'date_to': {
    #                         'tagname': 'date_to',
    #                         'alias_name': 'Дата конца',
    #                         'alias_nameKZ': 'Аяқталу күні',
    #                     },
    #                 },
    #             },
    #         ]
    #     }
    # },
    # {
    #     'action_name': 'Добавление классной квалификации',
    #     'action_nameKZ': 'Сыныптық квалификацияны қосу',
    #     'action_type': 'add_coolness',
    #     'children': [
    #         {
    #             'alias_name': 'Классная квалификация для добавления',
    #             'alias_nameKZ': 'Қосу үшін сыныптық квалификация',
    #             'tagname': 'coolness',
    #             'data_taken': 'dropdown',
    #             'field_name': 'coolnesses',
    #         },
    #     ],
    #     'properties': {
    #         'coolness': {
    #             'alias_name': 'Классная квалификация для добавления',
    #             'alias_nameKZ': 'Қосу үшін сыныптық квалификация',
    #             'type': 'write',
    #             'data_taken': 'dropdown',
    #             'field_name': 'coolnesses',
    #         },
    #     },
    #     'actions': {
    #         'args': [
    #             {
    #                 'add_coolness': {
    #                     'coolness': {
    #                         'tagname': 'coolness',
    #                         'alias_name': 'Классная квалификация для добавления',
    #                         'alias_nameKZ': 'Қосу үшін сыныптық квалификация',
    #                     },
    #                 },
    #             },
    #         ],
    #     },
    # },
    # {
    #     'action_name': 'Понижение классной квалификации',
    #     'action_nameKZ': 'Сыныптық квалификацияны төмендету',
    #     'action_type': 'decrease_coolness',
    #     'children': [
    #         {
    #             'alias_name': 'Классная квалификация для понижения',
    #             'alias_nameKZ': 'Төмендету үшін сыныптық квалификация',
    #             'tagname': 'coolness',
    #             'data_taken': 'dropdown',
    #             'field_name': 'coolnesses',
    #         },
    #     ],
    #     'properties': {
    #         'coolness': {
    #             'alias_name': 'Классная квалификация для понижения',
    #             'alias_nameKZ': 'Төмендету үшін сыныптық квалификация',
    #             'type': 'delete',
    #             'data_taken': 'dropdown',
    #             'field_name': 'coolnesses',
    #         },
    #     },
    #     'actions': {
    #         'args': [
    #             {
    #                 'decrease_coolness': {
    #                     'coolness': {
    #                         'tagname': 'coolness',
    #                         'alias_name': 'Классная квалификация для понижения',
    #                         'alias_nameKZ': 'Төмендету үшін сыныптық квалификация',
    #                     },
    #                 },
    #             },
    #         ],
    #     },
    # },
    # {
    #     'action_name': 'Лишение классной квалификации',
    #     'action_nameKZ': 'Сыныптық квалификациядан босату',
    #     'action_type': 'delete_coolness',
    #     'children': [
    #         {
    #             'alias_name': 'Классная квалификация для лишения',
    #             'alias_nameKZ': 'Босату үшін сыныптық квалификация',
    #             'tagname': 'coolness',
    #             'data_taken': 'dropdown',
    #             'field_name': 'coolnesses',
    #         },
    #     ],
    #     'properties': {
    #         'coolness': {
    #             'alias_name': 'Классная квалификация для лишения',
    #             'alias_nameKZ': 'Босату үшін сыныптық квалификация',
    #             'type': 'delete',
    #             'data_taken': 'dropdown',
    #             'field_name': 'coolnesses',
    #         },
    #     },
    #     'actions': {
    #         'args': [
    #             {
    #                 'delete_coolness': {
    #                     'coolness': {
    #                         'tagname': 'coolness',
    #                         'alias_name': 'Классная квалификация для лишения',
    #                         'alias_nameKZ': 'Босату үшін сыныптық квалификация',
    #                     },
    #                 },
    #             },
    #         ],
    #     },
    # },
    {
        'action_name': 'Назначение на должность',
        'action_nameKZ': 'Қызметке тағайындау',
        'action_type': 'position_change',
        'children': [
            {
                'alias_name': 'Новая должность',
                'alias_nameKZ': 'Жаңа қызмет атауы',
                'tagname': 'staff_unit',
                'data_taken': 'dropdown',
                'field_name': 'staff_unit',
            }, {
                'alias_name': 'Процент надбавки',
                'alias_nameKZ': 'Қосымша пайыз',
                'tagname': 'percent',
                'data_taken': 'manual',
                'data_type': 'number'
            }, {
                'alias_name': 'Причина надбавки',
                'alias_nameKZ': 'Қосымша пайыздың себебі',
                'tagname': 'reason',
                'data_taken': 'manual',
                'data_type': 'string'
            }
        ],
        'properties': {
            'staff_unit': {
                'alias_name': 'Новая должность',
                'alias_nameKZ': 'Жаңа қызмет атауы',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'staff_unit',
            },
            'percent': {
                'alias_name': 'Процент надбавки',
                'alias_nameKZ': 'Қосымша пайыз',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'number',
            },
            'reason': {
                'alias_name': 'Причина надбавки',
                'alias_nameKZ': 'Қосымша пайыздың себебі',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'string',
            }
        },
        'actions': {
            'args': [
                {
                    'position_change': {
                        'staff_unit': {
                            'tagname': 'staff_unit',
                            'alias_name': 'Новая должность',
                            'alias_nameKZ': 'Жаңа қызмет атауы',
                        },
                        'percent': {
                            'tagname': 'percent',
                            'alias_name': 'Процент надбавки',
                            'alias_nameKZ': 'Қосымша пайыз',
                        },
                        'reason': {
                            'tagname': 'reason',
                            'alias_name': 'Причина надбавки',
                            'alias_nameKZ': 'Қосымша пайыздың себебі',
                        }
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Присвоение звания',
        'action_nameKZ': 'Дәреже тағайындау',
        'action_type': 'increase_rank',
        'children': [
            {
                'alias_name': 'Звание для повышения',
                'alias_nameKZ': 'Арттыру үшін Дәреже',
                'tagname': 'rank',
                'data_taken': 'dropdown',
                'field_name': 'rank',
            },
        ],
        'properties': {
            'rank': {
                'alias_name': 'Звание для повышения',
                'alias_nameKZ': 'Арттыру үшін Дәреже',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'rank',
            },
        },
        'actions': {
            'args': [
                {
                    'increase_rank': {
                        'rank': {
                            'tagname': 'rank',
                            'alias_name': 'Звание для повышения',
                            'alias_nameKZ': 'Арттыру үшін Дәреже',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Понижение звания',
        'action_nameKZ': 'Дәреже төмендету',
        'action_type': 'decrease_rank',
        'children': [
            {
                'alias_name': 'Звание для понижения',
                'alias_nameKZ': 'Төмендету үшін дәреже',
                'tagname': 'rank',
                'data_taken': 'dropdown',
                'field_name': 'rank',
            },
        ],
        'properties': {
            'rank': {
                'alias_name': 'Звание для понижения',
                'alias_nameKZ': 'Төмендету үшін дәреже',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'rank',
            },
        },
        'actions': {
            'args': [
                {
                    'decrease_rank': {
                        'rank': {
                            'tagname': 'rank',
                            'alias_name': 'Звание для понижения',
                            'alias_nameKZ': 'Төмендету үшін дәреже',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Смена статуса на постоянный',
        'action_nameKZ': 'Тұрақты мәртебеге өзгерту',
        'action_type': 'status_change',
        'children': [
            {
                'alias_name': 'Статус',
                'alias_nameKZ': 'Мәртебе',
                'tagname': 'rank',
                'data_taken': 'dropdown',
                'field_name': 'statuses',
            },
        ],
        'properties': {
            'status': {
                'alias_name': 'Статус',
                'alias_nameKZ': 'Мәртебе',
                'type': 'write',
                'data_taken': 'dropdown',
                'field_name': 'statuses',
            },
        },
        'actions': {
            'args': [
                {
                    'status_change': {
                        'status': {
                            'tagname': 'status',
                            'alias_name': 'Статус',
                            'alias_nameKZ': 'Мәртебе',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Отпуск по болезни',
        'action_nameKZ': 'Ауру демалысы',
        'action_type': 'sick_leave',
        'children': [
            {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'tagname': 'date_from',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'tagname': 'date_to',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        ],
        'properties': {
            'date_from': {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            'date_to': {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'type': 'read',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        },
        'actions': {
            'args': [
                {
                    'sick_leave': {
                        'date_from': {
                            'tagname': 'date_from',
                            'alias_name': 'Дата начала',
                            'alias_nameKZ': 'Басталу күні',
                        },
                        'date_to': {
                            'tagname': 'date_to',
                            'alias_name': 'Дата конца',
                            'alias_nameKZ': 'Аяқталу күні',
                        },
                    },
                },
            ],
        },
    },
    {
        'action_name': 'Отпуск по болезни',
        'action_nameKZ': 'Ауру демалысы',
        'action_type': 'sick_leave',
        'children': [
            {
                'alias_name': 'Дата начала',
                'alias_nameKZ': 'Басталу күні',
                'tagname': 'date_from',
                'data_taken': 'manual',
                'data_type': 'date',
            },
            {
                'alias_name': 'Дата конца',
                'alias_nameKZ': 'Аяқталу күні',
                'tagname': 'date_to',
                'data_taken': 'manual',
                'data_type': 'date',
            },
        ],
        'properties': {
            "surname":{
                "alias_nameKZ":"Тегі",
                "data_taken":"auto",
                "type":"write",
                "field_name":"surname",
                "to_tags":{
                    "titleKZ":"Тегі",
                    "isHidden":"false"
                }
            },
            "name":{
                "alias_nameKZ":"Аты",
                "data_taken":"auto",
                "type":"write",
                "field_name":"name",
                "to_tags":{
                    "titleKZ":"Аты",
                    "isHidden":False
                }
            },
            "father":{
                "alias_nameKZ":"Әкесінің аты",
                "data_taken":"auto",
                "type":"write",
                "field_name":"father_name",
                "to_tags":{
                    "foundInText":"Отчество субъекта",
                    "titleKZ":"Әкесінің аты",
                    "isHidden":False,
                    "cases":0
                }
            },
            "contract":{
                "to_tags":{
                    "tagname":"contract",
                    "titleKZ":"Контракт",
                    "idToChange":"1687429527959",
                    "id":"1687429527959",
                    "foundInText":"{{contract - term}}",
                    "isHidden":False,
                    "cases":0,
                    "action_type":"[renew_contract]"
                },
                "alias_name":"Контракт",
                "alias_nameKZ":"Контракт",
                "type":"write",
                "data_taken":"dropdown",
                "field_name":"contracts",
                "isHidden":False
            },
            "new_position":{
                "alias_nameKZ":"Жаңа позиция",
                "data_taken":"dropdown",
                "type":"write",
                "field_name":"staff_unit",
                "to_tags":{
                    "titleKZ":"Жаңа позиция",
                    "directory":"staff_unit",
                    "isHidden":"false"
                }
            }
            },
        'actions': {
            'args': [
                {
                    "apply_candidate":{
                        "staff_unit":{
                            "tagname":"new_position",
                            "alias_name":"Новая должность",
                            "alias_nameKZ":"Жаңа қызмет атауы"
                        },
                        "contract":{
                            "tagname":"contract_type",
                            "alias_name":"Контракт",
                            "alias_nameKZ":"Контракт"
                        },
                    },
                },
            ],
        },
    },
    {
        'data_taken': 'auto',
        'properties': [
            {
                'alias_name': 'Отчество субъекта',
                'alias_nameKZ': 'Әкесінің аты',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'father_name',
            },
            {
                'alias_name': 'Имя субъекта',
                'alias_nameKZ': 'Аты',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'name',
            },
            {
                'alias_name': 'Фамилия субъекта',
                'alias_nameKZ': 'Тегі',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'surname',
            },
            {
                'alias_name': 'Звание',
                'alias_nameKZ': 'Дәреже',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'rank',
            },
            {
                'alias_name': 'Позиция',
                'alias_nameKZ': 'Позиция',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'position',
            },
            {
                'alias_name': 'Офицерский номер субъекта',
                'alias_nameKZ': 'Субъект қызметкерінің нөмірі',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'officer_number',
            },
            {
                'alias_name': 'Дата рождения',
                'alias_nameKZ': 'Tуған күні',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'date-of-living',
            },
            {
                'alias_name': 'Выслуга лет (годы)',
                'alias_nameKZ': 'Қызмет өтілі (жыл)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'length-of-service-year',
            },
            {
                'alias_name': 'Выслуга лет (месяца)',
                'alias_nameKZ': 'Қызмет өтілі (айлар)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'length-of-service-month',
            },
            {
                'alias_name': 'Выслуга лет (дни)',
                'alias_nameKZ': 'Қызмет өтілі (күндер)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'length-of-service-day',
            },
            {
                'alias_name': 'Стаж работы фактический (года)',
                'alias_nameKZ': 'Нақты жұмыс өтілі (жыл)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'length-of-work-year',
            },
            {
                'alias_name': 'Стаж работы фактический (месяца)',
                'alias_nameKZ': 'Нақты жұмыс өтілі (айлар)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'length-of-work-month',
            },
            {
                'alias_name': 'Нақты жұмыс өтілі (күндер)',
                'alias_nameKZ': 'Стаж работы фактический (дни)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'length-of-work-day',
            },
            {
                'alias_name': 'Еңбек өтілі және еңбек өтілі (жылдар)',
                'alias_nameKZ': 'Стаж работы в сумме с выслугой лет (годы)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'total-of-service-year',
            },
            {
                'alias_name': 'Еңбек өтілі және еңбек өтілі (айлар)',
                'alias_nameKZ': 'Стаж работы в сумме с выслугой лет (месяца)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'total-of-service-month',
            },
            {
                'alias_name': 'Еңбек өтілі және еңбек өтілі (күндер)',
                'alias_nameKZ': 'Стаж работы в сумме с выслугой лет (дни)',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'total-of-service-day',
            },
            {
                'alias_name': 'Данные о семье',
                'alias_nameKZ': 'Отбасы деректері',
                'type': 'read',
                'data_taken': 'auto',
                'auto_name': 'family_member',
            },
        ],
    },
]
