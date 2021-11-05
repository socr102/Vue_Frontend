<template>
  <div id="recommendations">
    <h2>Product recommendations</h2>
    <div class="main-articles-sold">
      <div class="top-section">
        <div class="badges">
          <span
            class="badge bg-primary"
            v-for="item in Material_types"
            :key="item.id"
            >{{ item }} <a href="#"><CancelIcon /></a
          ></span>
          <!-- <span class="badge bg-primary">Packtejp, Häftapparater &amp; Limp  <a href="#"><CancelIcon /></a></span>
        <span class="badge bg-primary">Kartonger &amp; Transportlådor  <a href="#"><CancelIcon /></a></span> -->
          <button class="btn btn-outline-dark mx-2">+</button>
        </div>
        <p class="persentage">54%</p>
      </div>
      <div class="toggle-holder">
        <button
          class="btn btn-primary"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#soldarticles"
          aria-expanded="false"
          aria-controls="soldarticles"
        >
          More sold articles
        </button>
        <div class="collapse recommended-collapse" id="soldarticles">
          <div class="inner-collapse">
            <div class="holder" v-for="(item,index) in Recommendations" :key="index">
              <h3><RecommendedIcon /> Recommended</h3>
              <button
                class="btn btn-primary"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="'#ar_' +index"
                aria-expanded="false"
                aria-controls="articleone"
              >
                <div class="toggle-head">
                  <div class="table-layout">
                    <div class="table-head">
                      <div>Article number</div>
                      <div>Article Name</div>
                      <div>Сategory</div>
                    </div>
                    <div class="table-body">
                      <div class="table-holder" v-for="(article,article_index) in item.articles" :key="article_index">
                        <div>{{ article.Article_number }}</div>
                        <div>{{ article.Article_Name }}</div>
                        <div>{{ article.Category }}</div>
                      </div>
                    </div>
                  </div>
                  <div
                    class="article-connection"
                  >
                    <div class="article-head">Article connection</div>
                    <div class="value">{{ item.percentage }}</div>
                  </div>
                </div>
              </button>

              <div class="collapse" :id="'ar_'+index">
                <div class="py-4">
                  <strong class="mb-4 d-block text-left"
                    >Recommended associated products</strong
                  >
                  <div class="toggle-head-inner">
                    <div class="table-layout">
                      <div class="table-head">
                        <div>ID</div>
                        <div>Article Name</div>
                        <div>Сategory</div>
                        <div>Probability to sell</div>
                      </div>
                      <div class="table-body">
                        <div
                          class="table-holder"
                          v-for="item in item.products"
                          :key="item.id"
                        >
                          <div>{{ item.id }}</div>
                          <div>{{ item.Article_Name }}</div>
                          <div>{{ item.Сategory }}</div>
                          <div
                            v-bind:class="
                              item.Probability_to_sell == 'High'
                                ? 'bold-text text-success'
                                : item.Probability_to_sell == 'Medium'
                                ? 'bold-text text-warning'
                                : item.Probability_to_sell == 'Low'
                                ? 'bold-text text-danger'
                                : ''
                            "
                          >
                            {{ item.Probability_to_sell }}
                          </div>
                          <div class="button-holder">
                            <button class="btn btn-outline-primary">
                              <span>+</span> Add article
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CancelIcon from "../../icons/cancel.vue";
import RecommendedIcon from "../../icons/recommended.vue";

export default {
  name: "Recommendations",
  components: {
    CancelIcon,
    RecommendedIcon,
  },
  data: function () {
    return {
      Material_types: [
        "Förpackningsmaterial",
        "Packtejp, Häftapparater & Limp",
        "Kartonger & Transportlådor",
      ],

      Recommendations: [
        {
          articles: [
            {
              Article_number: "00139",
              Article_Name: "Tejp, påsförslutning Röd 66 m x 12 mm, 6 st",
              Category: "Förpackningsmaterial",
            },
            {
              Article_number: "00139",
              Article_Name: "Påsförslutare röd 12 mm",
              Category: "Packtejp, Häftapparater & Limp",
            },
          ],
          products: [
            {
              id: "20536",
              Article_Name: "Basket 26 l color blue",
              Сategory: "Förpackningsmaterial",
              Probability_to_sell: "High",
            },
            {
              id: "12072",
              Article_Name: "Skopa plast 900 ml",
              Сategory: "Packtejp, Häftapparater & Limp",
              Probability_to_sell: "Medium",
            },
            {
              id: "17147",
              Article_Name: "Påsförslutare röd 12 mm",
              Сategory: "Packtejp, Häftapparater & Limp",
              Probability_to_sell: "Low",
            },
          ],
          percentage:'50%'
        },
          {
          articles: [
            {
              Article_number: "00139",
              Article_Name: "Tejp, påsförslutning Röd 66 m x 12 mm, 6 st",
              Category: "Förpackningsmaterial",
            },
            {
              Article_number: "00139",
              Article_Name: "Påsförslutare röd 12 mm",
              Category: "Packtejp, Häftapparater & Limp",
            },
          ],
          products: [
            {
              id: "20536",
              Article_Name: "Basket 26 l color blue",
              Сategory: "Förpackningsmaterial",
              Probability_to_sell: "High",
            },
            {
              id: "12072",
              Article_Name: "Skopa plast 900 ml",
              Сategory: "Packtejp, Häftapparater & Limp",
              Probability_to_sell: "Medium",
            },
            {
              id: "17147",
              Article_Name: "Påsförslutare röd 12 mm",
              Сategory: "Packtejp, Häftapparater & Limp",
              Probability_to_sell: "Low",
            },
          ],
          percentage:'50%'
        },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
