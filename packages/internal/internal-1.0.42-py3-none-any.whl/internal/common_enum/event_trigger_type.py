from enum import Enum


class EventTriggerTypeEnum(str, Enum):
    MANUAL_CANCEL_SERVICE_TICKET = "manual_cancel_service_ticket"
    MANUAL_TRACING_START_SERVICE_TICKET = "manual_tracking_start_service_ticket"
    MANUAL_TRACING_STOP_SERVICE_TICKET = "manual_tracking_stop_service_ticket"
    MANUAL_CREATE_SERVICE_TICKET = "manual_create_service_ticket"
    MANUAL_IMPORT_RESERVATION_SMWS = "manual_import_reservation_smws"
    MANUAL_MODIFY_ESTIMATED_ARRIVAL_TIME_SERVICE_TICKET = "manual_modify_estimated_arrival_time_service_ticket"
    MANUAL_MODIFY_ESTIMATED_DELIVERY_TIME_SERVICE_TICKET = "manual_modify_estimated_delivery_time_service_ticket"
    MANUAL_BOOKING_MESSAGE_SERVICE_TICKET = "manual_booking_message_service_ticket"
    MANUAL_DELIVERY_MESSAGE_SERVICE_TICKET = "manual_delivery_message_service_ticket"

    CANCEL_SERVICE_TICKET = "cancel_service_ticket"
    IMPORT_RESERVATION_CONFLICT_AUTO_CANCEL = "import_reservation_conflict_auto_cancel"
    BOOKING_REMINDING_SERVICE_TICKET = "booking_reminding_service_ticket"
    LPNR_IN = "lpnr_in"
    LPNR_OUT = "lpnr_out"
