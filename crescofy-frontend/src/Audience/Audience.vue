<template>
<div class="page-wrapper">
    <div class="page-content-tab">
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="page-title-box">
                        <Grid/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Grid from './components/Grid';

export default {
  name: 'Audience',
  components: { Grid },
}
</script>