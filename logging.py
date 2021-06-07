LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filers': ['require_debug_true'],
            'verbose': {
                'format': '%(levelname)s %(acstime)s %(message)s %(pathname)s'
            }

        },
        'mail_admins': {
            'level': 'Error',
            'propagate': False,
            'verbose': {
                'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
            }
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'Warning',
            'propagate': True,
            'formatter': {
                'verbose': {
                    'format': '%(exc_info)s'
                }
            },
        },
        'general': {
            'django': {
                'level': 'INFO',
                'propagate': False,
                'formatter': {
                    'verbose': {
                        'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
                    }
                }
            },

        },
        'errors': {
            'django.request': {
                'level': 'Error',
                'handlers': ['mail_admins'],
                'propagate': True,
                'formatter': {
                    'verbose': {
                        'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'

                    }
                }
            },
            'django.server': {
                'level': 'Error',
                'handlers': ['mail_admins'],
                'propagate': True,
                'formatter': {
                    'verbose': {
                        'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'

                    }
                }
            },
            'django.template': {
                'level': 'Error',
                'propagate': True,
                'formatter': {
                    'verbose': {
                        'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'

                    }
                }
            },
            'django.db_backends': {
                'level': 'Error',
                'propagate': True,
                'formatter': {
                    'verbose': {
                        'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'

                    }
                }
            },
        },
        'security': {
            'django.security': {
                'level': 'Critical',
                'propagate': True,
                'formatter': {
                    'verbose': {
                        'format': '%(asctime)s %(levelname)s %(module)s %(message)s'

                    }
                }
            }
        }
    }
}
