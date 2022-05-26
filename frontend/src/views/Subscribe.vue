<template>
  <div class="subscribe">
    <a-card title="LeetCode" style="width: 800px; background:#ECECEC;">
      <a slot="extra" href="#"><a-icon key="pushpin" type="pushpin" /></a>
      <p id="left">力扣（LeetCode）是领扣网络旗下专注于程序员技术成长和企业技术人才服务的品牌。源自美国硅谷，力扣为全球程序员提供了专业的IT 技术职业化提升平台，有效帮助程序员实现快速进步和长期成长。</p>
    </a-card>
    <br />
    <a-card title="洛谷" style="width: 800px; background:#ECECEC;">
      <a slot="extra" href="#"><a-icon key="pushpin" type="pushpin" /></a>
      <p id="left">洛谷创办于2013年,致力于为参加noip、noi、acm的选手提供清爽、快捷的编程体验。它拥有在线测题系统、强大的社区、在线学习功能。很多教程内容由各位oiers提供的,内容广泛。</p>
    </a-card>
    <br />
    <a-card title="牛客网" style="width: 800px; background:#ECECEC;">
      <a slot="extra" href="#"><a-icon key="pushpin" type="pushpin" /></a>
      <p id="left">牛客网，是一个集笔面试系统、题库、课程教育、社群交流、招聘内推于一体的招聘类网站。
牛客网题库中包含几万道题目，主要通过第三方购买和 UGC 的方式获得，牛客网先后尝试了直播和录播课，内容覆盖笔试题解析、面试技巧和机器学习等。</p>
    </a-card>
    <br />
    <a-card title="AtCoder" style="width: 800px; background:#ECECEC;">
      <a slot="extra" href="#"><a-icon key="pushpin" type="pushpin" /></a>
      <p id="left">AtCoder是日本最大的算法竞技网站，正式创立于2012年6月20日，由AtCoder Inc.运行并维护，提供编程在线比赛、过往比赛提交、在线评测等服务。</p>
    </a-card>
    <br />
    <a-card title="CodeForces" style="width: 800px;background:#ECECEC;">
      <a slot="extra" href="#"><a-icon key="pushpin" type="pushpin" /></a>
      <p id="left">Codeforces是一家为计算机编程爱好者提供在线评测系统的俄罗斯网站。该网站由萨拉托夫国立大学的一个团体创立并负责运营。</p>
    </a-card>
  </div>
</template>

<style scoped>
.subscribe {
    width:800px;
    margin: 0 auto;
}

#left {
    text-align: left;
}

</style>