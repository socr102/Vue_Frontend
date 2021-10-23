<template>
<div class="container">
    <div class="row vh-100 d-flex justify-content-center">
        <div class="col-12 align-self-center">
            <div class="">
                <div class="card-body">
                    <div class="row">
                        <div class="col-lg-5 mx-auto">
                            <div class="card">
                                <div class="card-body">
                                    <div class="media mb-3">
                                        <a href="../analytics/analytics-index.html" class="logo logo-admin">
                                            <img src="../../public/assets/images/logo-sm.png" height="40" alt="logo" class="auth-logo">
                                        </a>
                                        <div class="media-body align-self-center text-truncate ml-2">
                                            <h4 class="mt-0 mb-1 font-weight-semibold text-dark font-18">Oops! Sorry page does not found</h4>
                                            <p class="text-muted  mb-0">Back to dashboard of Metrica.</p>
                                        </div><!--end media-body-->
                                    </div>
                                    <img src="../../public/assets/images/404.png" alt="" class="d-block mx-auto mt-4" height="250">
                                    <div class="text-center auth-logo-text mb-4">
                                        <h4 class="mt-0 mb-3 mt-5">Looks like you've got lost...</h4>
                                        <router-link class="btn btn-sm btn-primary" to="/">Back to Dashboard</router-link>
                                    </div> <!--end auth-logo-text-->
                                </div>
                            </div>
                        </div><!--end col-->
                    </div><!--end row-->
                </div><!--end card-body-->
            </div><!--end card-->
        </div><!--end col-->
    </div><!--end row-->
</div><!--end container-->
</template>

<script>

export default {
  name: '404',
}
</script>