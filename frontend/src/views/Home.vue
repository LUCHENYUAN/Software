<template>
  <div class="home">
    <a-carousel autoplay>
      <div><img src="../assets/bg.png" /></div>
      <div><img src="../assets/bg1.png" /></div>
      <div><img src="../assets/bg2.png" /></div>
      <div><img src="../assets/bg3.png" /></div>
    </a-carousel>
    <div class="competition">
      <h2>热门赛事</h2>
      <ul>
        <li>
          <a-card hoverable style="width: 300px">
            <img slot="cover" alt="example" src="../assets/card1.png" />
            <template slot="actions" class="ant-card-actions">
              <a-icon key="pushpin" type="pushpin" />
              <a-icon key="profile" type="profile" />
            </template>
            <a-card-meta title="洛谷" description="洛谷5月月赛Ⅰ"> </a-card-meta>
          </a-card>
        </li>
        <li id="margin-left">
          <a-card hoverable style="width: 300px">
            <img slot="cover" alt="example" src="../assets/card2.png" />
            <template slot="actions" class="ant-card-actions">
              <a-icon key="pushpin" type="pushpin" />
              <a-icon key="profile" type="profile" />
            </template>
            <a-card-meta title="洛谷" description="洛谷5月月赛Ⅱ"> </a-card-meta>
          </a-card>
        </li>
        <li id="margin-left">
          <a-card hoverable style="width: 300px">
            <img slot="cover" alt="example" src="../assets/pc_card.png" />
            <template slot="actions" class="ant-card-actions">
              <a-icon key="pushpin" type="pushpin" />
              <a-icon key="profile" type="profile" />
            </template>
            <a-card-meta title="LeetCode" description="第78场双周赛">
            </a-card-meta>
          </a-card>
        </li>
      </ul>
      <p></p>
      <p></p>
    </div>
  </div>
</template>

<style scoped>
.home {
  margin-bottom: 30px;
}

li {
  list-style: none;
  float: left;
  width: 300px;
}

.home > img {
  width: 400px;
  margin-top: 20px;
}

.competition {
  width: 1000px;
  margin: 0 auto;
}

h2 {
  text-align: left;
}

#margin-left {
  margin-left: 30px;
}

.ant-carousel >>> .slick-slide {
  /* height: 400px; */
  overflow: hidden;
}
.ant-carousel >>> .slick-slide img {
  margin: 0 auto;
  width: 100%;
}

/*.ant-carousel >>> .slick-slide {
  text-align: center;
  line-height: calc( 100% / 1700 * 520 );
  background: rgb(66, 66, 66);
  overflow: hidden;
}

.ant-carousel >>> .slick-slide h3 {
  color: #fff;
}

.ant-carousel >>> .custom-slick-arrow {
  width: 25px;
  height: 25px;
  font-size: 25px;
  color: #fff;
  background-color: rgba(31, 45, 61, 0.11);
  opacity: 0.3;
}

.ant-carousel >>> .custom-slick-arrow:before {
  display: none;
}
.ant-carousel >>> .custom-slick-arrow:hover {
  opacity: 0.5;
}*/
</style>