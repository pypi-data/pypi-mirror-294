import grpc
import jwt  # pip install pyJWT, ATTENTION, no pip install jwt!!
import time
import os
import logging
from datetime import datetime
from retry import retry

from . import auth_pb2
from . import auth_pb2_grpc

# CONSTANTS
BX_HEADER_TOKEN_NAME = "bx_token"
CHANNEL_TIMEOUT = 40  # In seconds
LOGGER = logging.getLogger('batchx');

# CONFIG
CALL_DELAY = 0.5      # Initial delay (in seconds) between remote method call attempts.
CALL_BACKOFF = 2      # Multiplier applied to delay between attempts.
CALL_MAX_DELAY = 60   # Maximum value of delay (in seconds).
MAX_TRIES = 10        # The maximum number of attempts. default: -1 (infinite).
CALL_TIMEOUT = 60     # Unary call timeout in seconds.

channel = None  # Connection managed at module level. One common channel for all service classes within the module.
bx_token = None
access_token = None
bx_endpoint = None


class RecoverableException(Exception):
    """Raised when a recoverable error occurs.
    It's used just to detect failed connections attempts and try again.
    So, do nothing.
    """
    pass


def is_recoverable(exception):
    if exception is None or exception.code() is None:
        return False
    if grpc.StatusCode.PERMISSION_DENIED == exception.code():
        return check()
    return grpc.StatusCode.NOT_FOUND != exception.code() and \
           grpc.StatusCode.ALREADY_EXISTS != exception.code() and \
           grpc.StatusCode.UNKNOWN != exception.code() and \
           grpc.StatusCode.INVALID_ARGUMENT != exception.code() and \
           grpc.StatusCode.FAILED_PRECONDITION != exception.code() and \
           grpc.StatusCode.UNAUTHENTICATED != exception.code()


def connect():
    connect_to(os.environ["BATCHX_ENDPOINT"], os.environ["BATCHX_TOKEN"], "BATCHX_SECURE_CONNECTION" not in os.environ.keys() or os.environ["BATCHX_SECURE_CONNECTION"]!="OFF");

@retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
def connect_to(endpoint, token, secure):
    global channel, bx_token, bx_endpoint
    if channel is None:
        try:
            if secure:
                channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials(), options={
                    "grpc.keepalive_time_ms": 30000,
                    'grpc.keepalive_timeout_ms': 30*60*1000,
                    'grpc.keepalive_permit_without_calls': True
                }.items())
            else:
                channel = grpc.insecure_channel(endpoint)
            grpc.channel_ready_future(channel).result(CHANNEL_TIMEOUT)
        except grpc.FutureTimeoutError as exc:
            channel = None
            raise RecoverableException
    bx_token = token
    bx_endpoint = endpoint


def channel_is_working():
    global channel
    if channel is not None:
        try:
            grpc.channel_ready_future(channel).result(CHANNEL_TIMEOUT)
            return True
        except grpc.FutureTimeoutError:
            pass
    return False


def current_access_token_is_valid():
    global access_token
    if access_token is None:
        return False
    else:
        access_token_dict = jwt.decode(access_token, options={"verify_signature":False})
        return access_token_dict['exp'] > time.time()

# Refreshes the current token. Returns False if it was already valid
def check():
    """Check whether there exist a working channel and a valid access token."""
    global bx_endpoint, bx_token
    if not channel_is_working() and bx_endpoint is not None and bx_token is not None:
        connect(bx_endpoint, bx_token)
    if not current_access_token_is_valid():
        login()
        return True
    return False


@retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
def make_call(func, request, auth_required=True, include_timeout=True):
    """Wrapper to manage remote method calls. It implements a retry policy with exponential backoff.

    :param str func: Function in charge of calling remote methods.
    :param str request: grpc message.
    :param str auth_required: if set to True or not passed, token header will be sent.
    :param str include_timeout: if set to True or not passed, default GRPC deadline will be set.
    :return: response returned by executing the function passed as parameter (func).
    """
    try:
        if include_timeout:
            timeout = CALL_TIMEOUT
        else:
            timeout = None;
        if auth_required:
            return func(request, metadata=[(BX_HEADER_TOKEN_NAME, access_token)], timeout=timeout)
        else:
            return func(request, timeout=timeout)
    except grpc.RpcError as exc:
        if is_recoverable(exc):
            raise RecoverableException  # If error is recoverable, retry call
        else:
            raise exc


def login():
    """ Connect to server and obtain an access token if needed."""
    global channel, bx_token, access_token
    if bx_token is not None:
        token = jwt.decode(bx_token, options={"verify_signature":False});
        if token['batchx-token-type'] == 'refresh':
            request_data = auth_pb2.RefreshTokenRequest(user_name=token['batchx-id'], refresh_token=bx_token)
            response = make_call(auth_pb2_grpc.AuthServiceStub(channel).RefreshToken, request_data, auth_required=False)
            access_token = response.access_token
        else:
            access_token = bx_token
    else:
        raise Exception("Batchx token not set. Please run: bx.connect()")


from . import token_pb2
from . import token_pb2_grpc
class TokenService:

    def AddTokenRequest(self, **kwargs):
        return token_pb2.AddTokenRequest(**kwargs)

    def AddTokenResponse(self, **kwargs):
        return token_pb2.AddTokenResponse(**kwargs)


from . import job_pb2
from . import job_pb2_grpc
class JobService:

    def CancelRequest(self, **kwargs):
        return job_pb2.CancelRequest(**kwargs)

    def CancelResponse(self, **kwargs):
        return job_pb2.CancelResponse(**kwargs)

    def CloseWorkflowRequest(self, **kwargs):
        return job_pb2.CloseWorkflowRequest(**kwargs)

    def CloseWorkflowResponse(self, **kwargs):
        return job_pb2.CloseWorkflowResponse(**kwargs)

    def CreateWorkflowRequest(self, **kwargs):
        return job_pb2.CreateWorkflowRequest(**kwargs)

    def CreateWorkflowResponse(self, **kwargs):
        return job_pb2.CreateWorkflowResponse(**kwargs)

    def DeleteRequest(self, **kwargs):
        return job_pb2.DeleteRequest(**kwargs)

    def DeleteResponse(self, **kwargs):
        return job_pb2.DeleteResponse(**kwargs)

    def DeleteWorkflowRequest(self, **kwargs):
        return job_pb2.DeleteWorkflowRequest(**kwargs)

    def DeleteWorkflowResponse(self, **kwargs):
        return job_pb2.DeleteWorkflowResponse(**kwargs)

    def GetComputationalCostRequest(self, **kwargs):
        return job_pb2.GetComputationalCostRequest(**kwargs)

    def GetComputationalCostResponse(self, **kwargs):
        return job_pb2.GetComputationalCostResponse(**kwargs)

    def GetJobRequest(self, **kwargs):
        return job_pb2.GetJobRequest(**kwargs)

    def GetJobResponse(self, **kwargs):
        return job_pb2.GetJobResponse(**kwargs)

    def GetLogsRequest(self, **kwargs):
        return job_pb2.GetLogsRequest(**kwargs)

    def GetWorkflowGraphRequest(self, **kwargs):
        return job_pb2.GetWorkflowGraphRequest(**kwargs)

    def GetWorkflowGraphResponse(self, **kwargs):
        return job_pb2.GetWorkflowGraphResponse(**kwargs)

    def GetWorkflowRequest(self, **kwargs):
        return job_pb2.GetWorkflowRequest(**kwargs)

    def GetWorkflowResponse(self, **kwargs):
        return job_pb2.GetWorkflowResponse(**kwargs)

    def Job(self, **kwargs):
        return job_pb2.Job(**kwargs)

    def JobEvent(self, **kwargs):
        return job_pb2.JobEvent(**kwargs)

    def JobStateMessage(self, **kwargs):
        return job_pb2.JobStateMessage(**kwargs)

    def ListJobsRequest(self, **kwargs):
        return job_pb2.ListJobsRequest(**kwargs)

    def ListJobsResponse(self, **kwargs):
        return job_pb2.ListJobsResponse(**kwargs)

    def ListLogsRequest(self, **kwargs):
        return job_pb2.ListLogsRequest(**kwargs)

    def ListLogsResponse(self, **kwargs):
        return job_pb2.ListLogsResponse(**kwargs)

    def ListWorkflowsRequest(self, **kwargs):
        return job_pb2.ListWorkflowsRequest(**kwargs)

    def ListWorkflowsResponse(self, **kwargs):
        return job_pb2.ListWorkflowsResponse(**kwargs)

    def StreamRequest(self, **kwargs):
        return job_pb2.StreamRequest(**kwargs)

    def StreamResponse(self, **kwargs):
        return job_pb2.StreamResponse(**kwargs)

    def SubmitRequest(self, **kwargs):
        return job_pb2.SubmitRequest(**kwargs)

    def SubmitResponse(self, **kwargs):
        return job_pb2.SubmitResponse(**kwargs)

    def TagJobRequest(self, **kwargs):
        return job_pb2.TagJobRequest(**kwargs)

    def TagJobResponse(self, **kwargs):
        return job_pb2.TagJobResponse(**kwargs)

    def TagWorkflowRequest(self, **kwargs):
        return job_pb2.TagWorkflowRequest(**kwargs)

    def TagWorkflowResponse(self, **kwargs):
        return job_pb2.TagWorkflowResponse(**kwargs)

    def Workflow(self, **kwargs):
        return job_pb2.Workflow(**kwargs)


from . import health_pb2
from . import health_pb2_grpc
class HealthService:

    def HealthCheckRequest(self, **kwargs):
        return health_pb2.HealthCheckRequest(**kwargs)

    def HealthCheckResponse(self, **kwargs):
        return health_pb2.HealthCheckResponse(**kwargs)


from . import tag_pb2
from . import tag_pb2_grpc
class TagService:

    def CreateTagRequest(self, **kwargs):
        return tag_pb2.CreateTagRequest(**kwargs)

    def CreateTagResponse(self, **kwargs):
        return tag_pb2.CreateTagResponse(**kwargs)

    def DeleteTagRequest(self, **kwargs):
        return tag_pb2.DeleteTagRequest(**kwargs)

    def DeleteTagResponse(self, **kwargs):
        return tag_pb2.DeleteTagResponse(**kwargs)

    def DisableTagRequest(self, **kwargs):
        return tag_pb2.DisableTagRequest(**kwargs)

    def DisableTagResponse(self, **kwargs):
        return tag_pb2.DisableTagResponse(**kwargs)

    def GetTagRequest(self, **kwargs):
        return tag_pb2.GetTagRequest(**kwargs)

    def GetTagResponse(self, **kwargs):
        return tag_pb2.GetTagResponse(**kwargs)

    def ListEnvironmentTagsRequest(self, **kwargs):
        return tag_pb2.ListEnvironmentTagsRequest(**kwargs)

    def ListEnvironmentTagsResponse(self, **kwargs):
        return tag_pb2.ListEnvironmentTagsResponse(**kwargs)

    def Tag(self, **kwargs):
        return tag_pb2.Tag(**kwargs)

    def TagCoordinates(self, **kwargs):
        return tag_pb2.TagCoordinates(**kwargs)

    def TagData(self, **kwargs):
        return tag_pb2.TagData(**kwargs)

    def UpdateTagRequest(self, **kwargs):
        return tag_pb2.UpdateTagRequest(**kwargs)

    def UpdateTagResponse(self, **kwargs):
        return tag_pb2.UpdateTagResponse(**kwargs)


from . import docker_pb2
from . import docker_pb2_grpc
class DockerService:

    def DockerImageCoordinates(self, **kwargs):
        return docker_pb2.DockerImageCoordinates(**kwargs)


from . import profile_pb2
from . import profile_pb2_grpc
class ProfileService:

    def Profile(self, **kwargs):
        return profile_pb2.Profile(**kwargs)


from . import user_pb2
from . import user_pb2_grpc
class UserService:

    def GetUserRequest(self, **kwargs):
        return user_pb2.GetUserRequest(**kwargs)

    def GetUserResponse(self, **kwargs):
        return user_pb2.GetUserResponse(**kwargs)

    def UpdateUserRequest(self, **kwargs):
        return user_pb2.UpdateUserRequest(**kwargs)

    def UpdateUserResponse(self, **kwargs):
        return user_pb2.UpdateUserResponse(**kwargs)


from . import auth_pb2
from . import auth_pb2_grpc
class AuthService:

    def ConfirmForgotPassword(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ConfirmForgotPassword, request)

    def ConfirmSignup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ConfirmSignup, request)

    def ForgotPassword(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ForgotPassword, request)

    def GoogleSignin(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).GoogleSignin, request)

    def GoogleSignup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).GoogleSignup, request)

    def Login(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).Login, request)

    def RefreshToken(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).RefreshToken, request)

    def ResendSignupConfirmationCode(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ResendSignupConfirmationCode, request)

    def RevokeRefreshToken(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).RevokeRefreshToken, request)

    def Signup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).Signup, request)

    def StartSignup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).StartSignup, request)

    def ConfirmForgotPasswordRequest(self, **kwargs):
        return auth_pb2.ConfirmForgotPasswordRequest(**kwargs)

    def ConfirmForgotPasswordResponse(self, **kwargs):
        return auth_pb2.ConfirmForgotPasswordResponse(**kwargs)

    def ConfirmSignupRequest(self, **kwargs):
        return auth_pb2.ConfirmSignupRequest(**kwargs)

    def ConfirmSignupResponse(self, **kwargs):
        return auth_pb2.ConfirmSignupResponse(**kwargs)

    def ForgotPasswordRequest(self, **kwargs):
        return auth_pb2.ForgotPasswordRequest(**kwargs)

    def ForgotPasswordResponse(self, **kwargs):
        return auth_pb2.ForgotPasswordResponse(**kwargs)

    def GoogleSigninRequest(self, **kwargs):
        return auth_pb2.GoogleSigninRequest(**kwargs)

    def GoogleSigninResponse(self, **kwargs):
        return auth_pb2.GoogleSigninResponse(**kwargs)

    def GoogleSignupRequest(self, **kwargs):
        return auth_pb2.GoogleSignupRequest(**kwargs)

    def GoogleSignupResponse(self, **kwargs):
        return auth_pb2.GoogleSignupResponse(**kwargs)

    def LoginRequest(self, **kwargs):
        return auth_pb2.LoginRequest(**kwargs)

    def LoginResponse(self, **kwargs):
        return auth_pb2.LoginResponse(**kwargs)

    def RefreshTokenRequest(self, **kwargs):
        return auth_pb2.RefreshTokenRequest(**kwargs)

    def RefreshTokenResponse(self, **kwargs):
        return auth_pb2.RefreshTokenResponse(**kwargs)

    def ResendSignupConfirmationCodeRequest(self, **kwargs):
        return auth_pb2.ResendSignupConfirmationCodeRequest(**kwargs)

    def ResendSignupConfirmationCodeResponse(self, **kwargs):
        return auth_pb2.ResendSignupConfirmationCodeResponse(**kwargs)

    def RevokeRefreshTokenRequest(self, **kwargs):
        return auth_pb2.RevokeRefreshTokenRequest(**kwargs)

    def RevokeRefreshTokenResponse(self, **kwargs):
        return auth_pb2.RevokeRefreshTokenResponse(**kwargs)

    def SignupRequest(self, **kwargs):
        return auth_pb2.SignupRequest(**kwargs)

    def SignupResponse(self, **kwargs):
        return auth_pb2.SignupResponse(**kwargs)

    def StartSignupRequest(self, **kwargs):
        return auth_pb2.StartSignupRequest(**kwargs)

    def StartSignupResponse(self, **kwargs):
        return auth_pb2.StartSignupResponse(**kwargs)

    def TokenResponse(self, **kwargs):
        return auth_pb2.TokenResponse(**kwargs)


from . import provider_pb2
from . import provider_pb2_grpc
class ProviderService:

    def GetMetricsRequest(self, **kwargs):
        return provider_pb2.GetMetricsRequest(**kwargs)

    def GetMetricsResponse(self, **kwargs):
        return provider_pb2.GetMetricsResponse(**kwargs)

    def ListPayoutsRequest(self, **kwargs):
        return provider_pb2.ListPayoutsRequest(**kwargs)

    def ListPayoutsResponse(self, **kwargs):
        return provider_pb2.ListPayoutsResponse(**kwargs)

    def ListRevenueByCustomerRequest(self, **kwargs):
        return provider_pb2.ListRevenueByCustomerRequest(**kwargs)

    def ListRevenueByCustomerResponse(self, **kwargs):
        return provider_pb2.ListRevenueByCustomerResponse(**kwargs)

    def ListRevenueByToolsRequest(self, **kwargs):
        return provider_pb2.ListRevenueByToolsRequest(**kwargs)

    def ListRevenueByToolsResponse(self, **kwargs):
        return provider_pb2.ListRevenueByToolsResponse(**kwargs)

    def Payout(self, **kwargs):
        return provider_pb2.Payout(**kwargs)


from . import billing_pb2
from . import billing_pb2_grpc
class BillingService:

    def CreatePaymentIntent(self, request):
        check()
        return make_call(billing_pb2_grpc.BillingServiceStub(channel).CreatePaymentIntent, request)

    def ListCharges(self, request):
        check()
        return make_call(billing_pb2_grpc.BillingServiceStub(channel).ListCharges, request)

    def Charge(self, **kwargs):
        return billing_pb2.Charge(**kwargs)

    def CreatePaymentIntentRequest(self, **kwargs):
        return billing_pb2.CreatePaymentIntentRequest(**kwargs)

    def CreatePaymentIntentResponse(self, **kwargs):
        return billing_pb2.CreatePaymentIntentResponse(**kwargs)

    def ListChargesRequest(self, **kwargs):
        return billing_pb2.ListChargesRequest(**kwargs)

    def ListChargesResponse(self, **kwargs):
        return billing_pb2.ListChargesResponse(**kwargs)


from . import organization_pb2
from . import organization_pb2_grpc
class OrganizationService:

    def CreateOrganizationRequest(self, **kwargs):
        return organization_pb2.CreateOrganizationRequest(**kwargs)

    def CreateOrganizationResponse(self, **kwargs):
        return organization_pb2.CreateOrganizationResponse(**kwargs)

    def DeleteInvitationRequest(self, **kwargs):
        return organization_pb2.DeleteInvitationRequest(**kwargs)

    def DeleteInvitationResponse(self, **kwargs):
        return organization_pb2.DeleteInvitationResponse(**kwargs)

    def DeleteMembershipRequest(self, **kwargs):
        return organization_pb2.DeleteMembershipRequest(**kwargs)

    def DeleteMembershipResponse(self, **kwargs):
        return organization_pb2.DeleteMembershipResponse(**kwargs)

    def GetOrganizationRequest(self, **kwargs):
        return organization_pb2.GetOrganizationRequest(**kwargs)

    def GetOrganizationResponse(self, **kwargs):
        return organization_pb2.GetOrganizationResponse(**kwargs)

    def HandleInvitationRequest(self, **kwargs):
        return organization_pb2.HandleInvitationRequest(**kwargs)

    def HandleInvitationResponse(self, **kwargs):
        return organization_pb2.HandleInvitationResponse(**kwargs)

    def Invitation(self, **kwargs):
        return organization_pb2.Invitation(**kwargs)

    def InviteMemberRequest(self, **kwargs):
        return organization_pb2.InviteMemberRequest(**kwargs)

    def InviteMemberResponse(self, **kwargs):
        return organization_pb2.InviteMemberResponse(**kwargs)

    def ListOrganizationInvitationsRequest(self, **kwargs):
        return organization_pb2.ListOrganizationInvitationsRequest(**kwargs)

    def ListOrganizationInvitationsResponse(self, **kwargs):
        return organization_pb2.ListOrganizationInvitationsResponse(**kwargs)

    def ListUserInvitationsRequest(self, **kwargs):
        return organization_pb2.ListUserInvitationsRequest(**kwargs)

    def ListUserInvitationsResponse(self, **kwargs):
        return organization_pb2.ListUserInvitationsResponse(**kwargs)

    def UpdateOrganizationRequest(self, **kwargs):
        return organization_pb2.UpdateOrganizationRequest(**kwargs)

    def UpdateOrganizationResponse(self, **kwargs):
        return organization_pb2.UpdateOrganizationResponse(**kwargs)


from . import audit_pb2
from . import audit_pb2_grpc
class AuditService:

    def ListEvents(self, request):
        check()
        return make_call(audit_pb2_grpc.AuditServiceStub(channel).ListEvents, request)

    def Event(self, **kwargs):
        return audit_pb2.Event(**kwargs)

    def ListEventsRequest(self, **kwargs):
        return audit_pb2.ListEventsRequest(**kwargs)

    def ListEventsResponse(self, **kwargs):
        return audit_pb2.ListEventsResponse(**kwargs)


from . import common_pb2
from . import common_pb2_grpc
class CommonService:

    def IntRangeFilter(self, **kwargs):
        return common_pb2.IntRangeFilter(**kwargs)

    def LongRangeFilter(self, **kwargs):
        return common_pb2.LongRangeFilter(**kwargs)

    def Organization(self, **kwargs):
        return common_pb2.Organization(**kwargs)

    def PageInfo(self, **kwargs):
        return common_pb2.PageInfo(**kwargs)

    def Picture(self, **kwargs):
        return common_pb2.Picture(**kwargs)

    def RateLimit(self, **kwargs):
        return common_pb2.RateLimit(**kwargs)

    def Region(self, **kwargs):
        return common_pb2.Region(**kwargs)

    def Thumbnail(self, **kwargs):
        return common_pb2.Thumbnail(**kwargs)

    def User(self, **kwargs):
        return common_pb2.User(**kwargs)


from . import consumer_pb2
from . import consumer_pb2_grpc
class ConsumerService:

    def GetMetrics(self, request):
        check()
        return make_call(consumer_pb2_grpc.ConsumerServiceStub(channel).GetMetrics, request)

    def GetMetricsRequest(self, **kwargs):
        return consumer_pb2.GetMetricsRequest(**kwargs)

    def GetMetricsResponse(self, **kwargs):
        return consumer_pb2.GetMetricsResponse(**kwargs)


from . import environment_pb2
from . import environment_pb2_grpc
class EnvironmentService:

    def GetEnvironment(self, request):
        check()
        return make_call(environment_pb2_grpc.EnvironmentServiceStub(channel).GetEnvironment, request)

    def IsIdAvailable(self, request):
        check()
        return make_call(environment_pb2_grpc.EnvironmentServiceStub(channel).IsIdAvailable, request)

    def ListRegions(self, request):
        check()
        return make_call(environment_pb2_grpc.EnvironmentServiceStub(channel).ListRegions, request)

    def GetEnvironmentRequest(self, **kwargs):
        return environment_pb2.GetEnvironmentRequest(**kwargs)

    def GetEnvironmentResponse(self, **kwargs):
        return environment_pb2.GetEnvironmentResponse(**kwargs)

    def IsIdAvailableRequest(self, **kwargs):
        return environment_pb2.IsIdAvailableRequest(**kwargs)

    def IsIdAvailableResponse(self, **kwargs):
        return environment_pb2.IsIdAvailableResponse(**kwargs)

    def ListRegionsRequest(self, **kwargs):
        return environment_pb2.ListRegionsRequest(**kwargs)

    def ListRegionsResponse(self, **kwargs):
        return environment_pb2.ListRegionsResponse(**kwargs)

    def Region(self, **kwargs):
        return environment_pb2.Region(**kwargs)


from . import filesystem_pb2
from . import filesystem_pb2_grpc
class FilesystemService:

    def AddS3Bucket(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).AddS3Bucket, request)

    def CancelUpload(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).CancelUpload, request)

    def CompleteUpload(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).CompleteUpload, request)

    def Copy(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).Copy, request)

    def DeleteFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).DeleteFile, request)

    def DownloadPresigned(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).DownloadPresigned, request)

    def GetBlob(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).GetBlob, request)

    def GetFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).GetFile, request)

    def ListBlobPointers(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListBlobPointers, request)

    def ListBlobs(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListBlobs, request)

    def ListFolder(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListFolder, request)

    def ListS3BucketFolder(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListS3BucketFolder, request)

    def ListS3Buckets(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListS3Buckets, request)

    def RemoveS3Bucket(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).RemoveS3Bucket, request)

    def ReportUploadStatus(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ReportUploadStatus, request)

    def SetBlobStatus(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).SetBlobStatus, request)

    def ShareFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ShareFile, request)

    def UploadPresigned(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).UploadPresigned, request)

    def AddS3BucketRequest(self, **kwargs):
        return filesystem_pb2.AddS3BucketRequest(**kwargs)

    def AddS3BucketResponse(self, **kwargs):
        return filesystem_pb2.AddS3BucketResponse(**kwargs)

    def Blob(self, **kwargs):
        return filesystem_pb2.Blob(**kwargs)

    def CancelUploadRequest(self, **kwargs):
        return filesystem_pb2.CancelUploadRequest(**kwargs)

    def CancelUploadResponse(self, **kwargs):
        return filesystem_pb2.CancelUploadResponse(**kwargs)

    def CompleteUploadRequest(self, **kwargs):
        return filesystem_pb2.CompleteUploadRequest(**kwargs)

    def CompleteUploadResponse(self, **kwargs):
        return filesystem_pb2.CompleteUploadResponse(**kwargs)

    def CopyRequest(self, **kwargs):
        return filesystem_pb2.CopyRequest(**kwargs)

    def CreateFolderRequest(self, **kwargs):
        return filesystem_pb2.CreateFolderRequest(**kwargs)

    def CreateFolderResponse(self, **kwargs):
        return filesystem_pb2.CreateFolderResponse(**kwargs)

    def DeleteFileRequest(self, **kwargs):
        return filesystem_pb2.DeleteFileRequest(**kwargs)

    def DeleteFileResponse(self, **kwargs):
        return filesystem_pb2.DeleteFileResponse(**kwargs)

    def DeleteFolderRequest(self, **kwargs):
        return filesystem_pb2.DeleteFolderRequest(**kwargs)

    def DeleteFolderResponse(self, **kwargs):
        return filesystem_pb2.DeleteFolderResponse(**kwargs)

    def DownloadPresignedRequest(self, **kwargs):
        return filesystem_pb2.DownloadPresignedRequest(**kwargs)

    def DownloadPresignedResponse(self, **kwargs):
        return filesystem_pb2.DownloadPresignedResponse(**kwargs)

    def File(self, **kwargs):
        return filesystem_pb2.File(**kwargs)

    def GetBlobRequest(self, **kwargs):
        return filesystem_pb2.GetBlobRequest(**kwargs)

    def GetBlobResponse(self, **kwargs):
        return filesystem_pb2.GetBlobResponse(**kwargs)

    def GetFileRequest(self, **kwargs):
        return filesystem_pb2.GetFileRequest(**kwargs)

    def GetFileResponse(self, **kwargs):
        return filesystem_pb2.GetFileResponse(**kwargs)

    def ListBlobPointersRequest(self, **kwargs):
        return filesystem_pb2.ListBlobPointersRequest(**kwargs)

    def ListBlobPointersResponse(self, **kwargs):
        return filesystem_pb2.ListBlobPointersResponse(**kwargs)

    def ListBlobsRequest(self, **kwargs):
        return filesystem_pb2.ListBlobsRequest(**kwargs)

    def ListBlobsResponse(self, **kwargs):
        return filesystem_pb2.ListBlobsResponse(**kwargs)

    def ListFolderRequest(self, **kwargs):
        return filesystem_pb2.ListFolderRequest(**kwargs)

    def ListFolderResponse(self, **kwargs):
        return filesystem_pb2.ListFolderResponse(**kwargs)

    def ListS3BucketFolderRequest(self, **kwargs):
        return filesystem_pb2.ListS3BucketFolderRequest(**kwargs)

    def ListS3BucketFolderResponse(self, **kwargs):
        return filesystem_pb2.ListS3BucketFolderResponse(**kwargs)

    def ListS3BucketsRequest(self, **kwargs):
        return filesystem_pb2.ListS3BucketsRequest(**kwargs)

    def ListS3BucketsResponse(self, **kwargs):
        return filesystem_pb2.ListS3BucketsResponse(**kwargs)

    def Metadata(self, **kwargs):
        return filesystem_pb2.Metadata(**kwargs)

    def RemoveS3BucketRequest(self, **kwargs):
        return filesystem_pb2.RemoveS3BucketRequest(**kwargs)

    def RemoveS3BucketResponse(self, **kwargs):
        return filesystem_pb2.RemoveS3BucketResponse(**kwargs)

    def ReportUploadStatusRequest(self, **kwargs):
        return filesystem_pb2.ReportUploadStatusRequest(**kwargs)

    def ReportUploadStatusResponse(self, **kwargs):
        return filesystem_pb2.ReportUploadStatusResponse(**kwargs)

    def S3BucketObject(self, **kwargs):
        return filesystem_pb2.S3BucketObject(**kwargs)

    def SetBlobStatusRequest(self, **kwargs):
        return filesystem_pb2.SetBlobStatusRequest(**kwargs)

    def SetBlobStatusResponse(self, **kwargs):
        return filesystem_pb2.SetBlobStatusResponse(**kwargs)

    def ShareFileRequest(self, **kwargs):
        return filesystem_pb2.ShareFileRequest(**kwargs)

    def ShareFileResponse(self, **kwargs):
        return filesystem_pb2.ShareFileResponse(**kwargs)

    def UploadPresignedRequest(self, **kwargs):
        return filesystem_pb2.UploadPresignedRequest(**kwargs)

    def UploadPresignedResponse(self, **kwargs):
        return filesystem_pb2.UploadPresignedResponse(**kwargs)


from . import picture_pb2
from . import picture_pb2_grpc
class PictureService:

    def CompleteUploadRequest(self, **kwargs):
        return picture_pb2.CompleteUploadRequest(**kwargs)

    def CompleteUploadResponse(self, **kwargs):
        return picture_pb2.CompleteUploadResponse(**kwargs)

    def CropPictureRequest(self, **kwargs):
        return picture_pb2.CropPictureRequest(**kwargs)

    def CropPictureResponse(self, **kwargs):
        return picture_pb2.CropPictureResponse(**kwargs)

    def UploadPresignedRequest(self, **kwargs):
        return picture_pb2.UploadPresignedRequest(**kwargs)

    def UploadPresignedResponse(self, **kwargs):
        return picture_pb2.UploadPresignedResponse(**kwargs)

    def UploadRequest(self, **kwargs):
        return picture_pb2.UploadRequest(**kwargs)

    def UploadResponse(self, **kwargs):
        return picture_pb2.UploadResponse(**kwargs)


from . import log_pb2
from . import log_pb2_grpc
class LogService:

    def LogRecord(self, **kwargs):
        return log_pb2.LogRecord(**kwargs)


from . import image_pb2
from . import image_pb2_grpc
class ImageService:

    def AreImageExamplesClonedRequest(self, **kwargs):
        return image_pb2.AreImageExamplesClonedRequest(**kwargs)

    def AreImageExamplesClonedResponse(self, **kwargs):
        return image_pb2.AreImageExamplesClonedResponse(**kwargs)

    def CloneImageExamplesRequest(self, **kwargs):
        return image_pb2.CloneImageExamplesRequest(**kwargs)

    def CloneImageExamplesResponse(self, **kwargs):
        return image_pb2.CloneImageExamplesResponse(**kwargs)

    def CloneImageRequest(self, **kwargs):
        return image_pb2.CloneImageRequest(**kwargs)

    def CloneImageResponse(self, **kwargs):
        return image_pb2.CloneImageResponse(**kwargs)

    def DeleteImageRequest(self, **kwargs):
        return image_pb2.DeleteImageRequest(**kwargs)

    def GetImageRequest(self, **kwargs):
        return image_pb2.GetImageRequest(**kwargs)

    def GetImageResponse(self, **kwargs):
        return image_pb2.GetImageResponse(**kwargs)

    def GetPushCredentialsRequest(self, **kwargs):
        return image_pb2.GetPushCredentialsRequest(**kwargs)

    def GetPushCredentialsResponse(self, **kwargs):
        return image_pb2.GetPushCredentialsResponse(**kwargs)

    def Image(self, **kwargs):
        return image_pb2.Image(**kwargs)

    def ImportImageRequest(self, **kwargs):
        return image_pb2.ImportImageRequest(**kwargs)

    def ListImageExamplesRequest(self, **kwargs):
        return image_pb2.ListImageExamplesRequest(**kwargs)

    def ListImageExamplesResponse(self, **kwargs):
        return image_pb2.ListImageExamplesResponse(**kwargs)

    def ListImagesRequest(self, **kwargs):
        return image_pb2.ListImagesRequest(**kwargs)

    def ListImagesResponse(self, **kwargs):
        return image_pb2.ListImagesResponse(**kwargs)

    def RemoveImageExampleRequest(self, **kwargs):
        return image_pb2.RemoveImageExampleRequest(**kwargs)

    def RemoveImageExampleResponse(self, **kwargs):
        return image_pb2.RemoveImageExampleResponse(**kwargs)

    def SearchImagesRequest(self, **kwargs):
        return image_pb2.SearchImagesRequest(**kwargs)

    def SearchImagesResponse(self, **kwargs):
        return image_pb2.SearchImagesResponse(**kwargs)

    def SetImageExampleRequest(self, **kwargs):
        return image_pb2.SetImageExampleRequest(**kwargs)

    def SetImageExampleResponse(self, **kwargs):
        return image_pb2.SetImageExampleResponse(**kwargs)

    def ShareImageRequest(self, **kwargs):
        return image_pb2.ShareImageRequest(**kwargs)

    def ShareImageResponse(self, **kwargs):
        return image_pb2.ShareImageResponse(**kwargs)

    def TagImageRequest(self, **kwargs):
        return image_pb2.TagImageRequest(**kwargs)

    def TagImageResponse(self, **kwargs):
        return image_pb2.TagImageResponse(**kwargs)


from . import alert_pb2
from . import alert_pb2_grpc
class AlertService:

    def DismissAlert(self, request):
        check()
        return make_call(alert_pb2_grpc.AlertServiceStub(channel).DismissAlert, request)

    def DismissAllAlerts(self, request):
        check()
        return make_call(alert_pb2_grpc.AlertServiceStub(channel).DismissAllAlerts, request)

    def ListAlerts(self, request):
        check()
        return make_call(alert_pb2_grpc.AlertServiceStub(channel).ListAlerts, request)

    def Alert(self, **kwargs):
        return alert_pb2.Alert(**kwargs)

    def DismissAlertRequest(self, **kwargs):
        return alert_pb2.DismissAlertRequest(**kwargs)

    def DismissAlertResponse(self, **kwargs):
        return alert_pb2.DismissAlertResponse(**kwargs)

    def DismissAllAlertsRequest(self, **kwargs):
        return alert_pb2.DismissAllAlertsRequest(**kwargs)

    def DismissAllAlertsResponse(self, **kwargs):
        return alert_pb2.DismissAllAlertsResponse(**kwargs)

    def ListAlertsRequest(self, **kwargs):
        return alert_pb2.ListAlertsRequest(**kwargs)

    def ListAlertsResponse(self, **kwargs):
        return alert_pb2.ListAlertsResponse(**kwargs)


from . import admin_pb2
from . import admin_pb2_grpc
class AdminService:

    def AddEnvironmentCredits(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).AddEnvironmentCredits, request)

    def CreateMembership(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateMembership, request)

    def CreateOrg(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateOrg, request)

    def CreateUser(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateUser, request)

    def GeneratePromoCode(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).GeneratePromoCode, request)

    def GetGlobalProperties(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).GetGlobalProperties, request)

    def RemoveUser(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).RemoveUser, request)

    def SetGlobalProperty(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).SetGlobalProperty, request)

    def AddEnvironmentCreditsRequest(self, **kwargs):
        return admin_pb2.AddEnvironmentCreditsRequest(**kwargs)

    def AddEnvironmentCreditsResponse(self, **kwargs):
        return admin_pb2.AddEnvironmentCreditsResponse(**kwargs)

    def Assignment(self, **kwargs):
        return admin_pb2.Assignment(**kwargs)

    def CreateMembershipRequest(self, **kwargs):
        return admin_pb2.CreateMembershipRequest(**kwargs)

    def CreateMembershipResponse(self, **kwargs):
        return admin_pb2.CreateMembershipResponse(**kwargs)

    def CreateOrgRequest(self, **kwargs):
        return admin_pb2.CreateOrgRequest(**kwargs)

    def CreateOrgResponse(self, **kwargs):
        return admin_pb2.CreateOrgResponse(**kwargs)

    def CreateUserRequest(self, **kwargs):
        return admin_pb2.CreateUserRequest(**kwargs)

    def CreateUserResponse(self, **kwargs):
        return admin_pb2.CreateUserResponse(**kwargs)

    def GeneratePromoCodeRequest(self, **kwargs):
        return admin_pb2.GeneratePromoCodeRequest(**kwargs)

    def GeneratePromoCodeResponse(self, **kwargs):
        return admin_pb2.GeneratePromoCodeResponse(**kwargs)

    def GetGlobalPropertiesRequest(self, **kwargs):
        return admin_pb2.GetGlobalPropertiesRequest(**kwargs)

    def GetGlobalPropertiesResponse(self, **kwargs):
        return admin_pb2.GetGlobalPropertiesResponse(**kwargs)

    def RemoveUserRequest(self, **kwargs):
        return admin_pb2.RemoveUserRequest(**kwargs)

    def RemoveUserResponse(self, **kwargs):
        return admin_pb2.RemoveUserResponse(**kwargs)

    def SetGlobalPropertyRequest(self, **kwargs):
        return admin_pb2.SetGlobalPropertyRequest(**kwargs)

    def SetGlobalPropertyResponse(self, **kwargs):
        return admin_pb2.SetGlobalPropertyResponse(**kwargs)

