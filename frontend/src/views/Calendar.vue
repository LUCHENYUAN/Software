<template>
  <div class="box">
    <li class="badges">
      <span class="preferChoice">
        偏好设置：
      <a-badge color="#ff3434" text="已预约"/>
      <a-switch default-checked @change="onChangeReserve"></a-switch>
      <a-badge color="#2aa8ec" text="已订阅"/>
      <a-switch default-checked @change="onChangeSubscribe"></a-switch>
      <a-badge color="white" text="其他可用赛事"/>
      <a-switch default-checked @change="onChangeNormal"></a-switch>
      </span>
      <span class="lengthChoice">
        比赛时长：
        <a-select default-value="1hr" style="width: 120px" @change="handleChangeLength">
          <a-select-option value="1hr">
          小于1小时
          </a-select-option>
          <a-select-option value="3hr">
          小于3小时
          </a-select-option>
          <a-select-option value="8hr">
          小于8小时
          </a-select-option>
          <a-select-option value="24hr">
          小于24小时
          </a-select-option>
          <a-select-option value="24hrm">
          大于24小时
          </a-select-option>
        </a-select>
      </span>
      <span class="DiffChoice">
        比赛难度：
        <a-select default-value="easy" style="width: 120px" @change="handleChangeDiff">
          <a-select-option value="easy">
          简单
          </a-select-option>
          <a-select-option value="medium">
          中等
          </a-select-option>
          <a-select-option value="hard">
          困难
          </a-select-option>
        </a-select>
      </span>
    </li>
    
  <a-calendar>
    <ul slot="dateCellRender" slot-scope="value" class="events">
      <li v-for="item in getListData(value)" :key="item.game_id">
        <a-popover :title=item.game_name trigger="click" placement="bottomLeft">
        <template slot="content"> 
          <p>平台：{{item.platform}}</p>
          <p>开始时间：{{item.game_start_time}}</p>
          <p v-if="item.game_end_time">结束时间：{{item.game_end_time}}</p>
          <p v-if="item.duration">时长：{{item.duration}}</p>
          <span>
            <p>链接：<a :href=item.website>{{item.website}}</a></p>
          </span>
          <a v-if="item.type != 'Reserve'" @click="ReserveGame" style="font-weight:bold">预约</a>
          <a v-if="item.type == 'Reserve'" @click="ReserveGameCancel" style="font-weight:bold" >取消预约</a>
        </template>
        <a-button :class=item.type type="primary">
          {{item.game_name}}
        </a-button>
        </a-popover>
      </li>
    </ul>
    <!--
    <template slot="monthCellRender" slot-scope="value">
      <div v-if="getMonthData(value)" class="notes-month">
        <section>{{ getMonthData(value) }}</section>
        <span>Backlog number</span>
      </div>
    </template>--->
  </a-calendar>
  <a-button type="primary" @click="showModal">
      上传自定义赛事
    </a-button>
    
    <a-modal v-model="modal_visible" title="填写自定义赛事信息">
      <a-form :form="form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }" @submit="handleSubmit">
    <a-form-item label="比赛名称">
      <a-input
        v-decorator="['note', { rules: [{ required: true, message: 'Please input your note!' }] }]"
      />
    </a-form-item>
    <a-form-item label="开始时间">
      <a-date-picker />
      <a-time-picker />
    </a-form-item>
    <a-form-item label="结束时间">
      <a-date-picker />
      <a-time-picker />
    </a-form-item>
    <a-form-item label="比赛链接">
      <a-input
        v-decorator="['note', { rules: [{ required: true, message: 'Please input your note!' }] }]"
      />
    </a-form-item>
    </a-form>
    </a-modal>
  </div>
</template>

<script>
import moment from 'moment';
export default {
  data() {
    return {
      needType: ['Reserve', 'Subscribe', 'Normal'],
       matches:[],
      visible: false,
      modal_visible: false,
    }
  },
  //接口
  /*mounted:function(){
      this.$http.get('http://127.0.0.1:5000/game/all').then((response)=>{
        console.log(response.data);
        this.matches=response.data;
      }).catch((response)=>{
        console.log(response);
      })
    },*/
  methods: {
    moment,
    hide() {
      this.visible = false
    },
    onChangeReserve() {
      let label = this.needType.indexOf('Reserve');
      if (label != -1) {
        this.needType.splice(label, 1);
        console.log('Reserve Deleted from needType!');
        console.log(this.needType);
      }
      else {
        this.needType.push('Reserve');
        console.log('Reserve Added to needType!');
        console.log(this.needType);
      }
    },
    onChangeSubscribe() {
      let label = this.needType.indexOf('Subscribe');
      if (label != -1) {
        this.needType.splice(label, 1);
        console.log('Subscribe Deleted from needType!');
        console.log(this.needType);
      }
      else {
        this.needType.push('Subscribe');
        console.log('Subscribe Added to needType!');
        console.log(this.needType);
      }
    },
    onChangeNormal() {
      let label = this.needType.indexOf('Normal');
      if (label != -1) {
        this.needType.splice(label, 1);
        console.log('Normal Deleted from needType!');
        console.log(this.needType);
      }
      else {
        this.needType.push('Normal');
        console.log('Normal Added to needType!');
        console.log(this.needType);
      }
    },
    ReserveGame(){

    },
    ReserveGameCancel() {

    },
    handleChangeDiff() {
      
    },
    handleChangeLength() {

    },
    getListData(value) {
      let listData = [];
      console.log(this.matches);
      let acquireData = [
        {game_id: 1, game_name:"「WHOI」Round 1", platform:"洛谷", game_start_time:"2022-05-15 14:00:00", game_end_time:"2022-05-15 18:00:00", duration:"", website:"https://www.luogu.com.cn/contest/67377", type:"Reserve"},
        {game_id: 2, game_name:"【LGR-109】洛谷 5 月月赛 II & Windy Round 6", platform:"洛谷", game_start_time:"2022-05-14 14:00:00", game_end_time:"2022-05-14 18:00:00", duration:"", website:"https://www.luogu.com.cn/contest/68326", type:"Subscribe"},
        {game_id: 3, game_name:"牛客小白月赛49", platform:"牛客网", game_start_time:"2022-05-06 19:00:00", game_end_time:"2022-05-06 21:00:00", duration:"", website:"https://ac.nowcoder.com/acm/contest/11226", type:"Normal"},
        {game_id: 4, game_name:"牛客挑战赛60", platform:"牛客网", game_start_time:"2022-05-13 19:00:00", game_end_time:"2022-05-13 22:00:00", duration:"", website:"https://ac.nowcoder.com/acm/contest/11200", type:"Normal"},
        {game_id: 5, game_name:"牛客小白月赛50", platform:"牛客网", game_start_time:"2022-05-21 20:00:00", game_end_time:"2022-05-21 22:00:00", duration:"", website:"https://ac.nowcoder.com/acm/contest/11227", type:"Normal"},
        {game_id: 6, game_name:"第 292 场周赛", platform:"LeetCode力扣", game_start_time:"2022-05-08 10:30:00", game_end_time:"2022-05-08 12:00:00", duration:"", website:"https://leetcode-cn.com/contest/weekly-contest-292", type:"Subscribe"},
        {game_id: 7, game_name:"第 78 场双周赛", platform:"LeetCode力扣", game_start_time:"2022-05-14 22:30:00", game_end_time:"2022-05-15 00:00:00", duration:"", website:"https://leetcode-cn.com/contest/biweekly-contest-78", type:"Subscribe"},
        {game_id: 8, game_name:"AtCoder Grand Contest 057", platform:"AtCoder", game_start_time:"2022-05-07 21:00:00", game_end_time:"", duration:"03:00", website:"https://atcoder.jp/contests/agc057", type:"Normal"},
        {game_id: 9, game_name:"AtCoder Beginner Contest 250", platform:"AtCoder", game_start_time:"2022-05-08 21:00:00", game_end_time:"", duration:"01:40", website:"https://atcoder.jp/contests/abc250", type:"Normal"},
        {game_id: 10, game_name:"Panasonic Programming Contest 2022(AtCoder Beginne", platform:"AtCoder", game_start_time:"2022-05-14 21:00:00", game_end_time:"", duration:"01:40", website:"https://atcoder.jp/contests/abc251", type:"Normal"},
        {game_id: 11, game_name:"AtCoder Regular Contest 140", platform:"AtCoder", game_start_time:"2022-05-15 21:00:00", game_end_time:"", duration:"02:00", website:"https://atcoder.jp/contests/arc140", type:"Reserve"},
        {game_id: 12, game_name:"AtCoder Beginner Contest 252", platform:"AtCoder", game_start_time:"2022-05-21 21:00:00", game_end_time:"", duration:"01:40", website:"https://atcoder.jp/contests/abc252", type:"Normal"},
        {game_id: 13, game_name:"AtCoder Heuristic Contest 011", platform:"AtCoder", game_start_time:"2022-05-28 12:00:00", game_end_time:"", duration:"199:00", website:"https://atcoder.jp/contests/ahc011", type:"Normal"},
        {game_id: 14, game_name:"Codeforces Round #788 (Div. 2)", platform:"CodeForces", game_start_time:"2022-05-06 22:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1670", type:"Reserve"},
        {game_id: 15, game_name:"Codeforces Round #789 (Div. 1)", platform:"CodeForces", game_start_time:"2022-05-08 22:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1677", type:"Normal"},
        {game_id: 16, game_name:"Codeforces Round #789 (Div. 2)", platform:"CodeForces", game_start_time:"2022-05-08 22:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1678", type:"Normal"},
        {game_id: 17, game_name:"Codeforces Round #790 (Div. 4)", platform:"CodeForces", game_start_time:"2022-05-10 22:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1676", type:"Normal"},
        {game_id: 18, game_name:"Educational Codeforces Round 128 (Rated for Div. 2", platform:"CodeForces", game_start_time:"2022-05-13 22:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1680", type:"Normal"},
        {game_id: 19, game_name:"Codeforces Round #791 (Div. 2)", platform:"CodeForces", game_start_time:"2022-05-14 17:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1679", type:"Normal"},
        {game_id: 20, game_name:"Educational Codeforces Round 129 (Rated for Div. 2", platform:"CodeForces", game_start_time:"2022-05-23 22:35:00", game_end_time:"", duration:"02:00", website:"https://codeforces.com/contests/1681", type:"Normal"}
      ];
      let judge = this.needType;
      //this.matches.forEach(function(record) {
      acquireData.forEach(function(record) {
        if (judge.indexOf(record.type) != -1) {
          //接口月份转换
          /*let monthString = record.game_start_time.slice(8,11);
          var monthParser = new Array();
          monthParser['Jan']=1;monthParser['Feb']=2;monthParser['Mar']=3;monthParser['Apr']=4;monthParser['May']=5;monthParser['Jun']=6;
          monthParser['Jul']=7;monthParser['Aug']=8;monthParser['Sep']=9;monthParser['Oct']=10;monthParser['Nov']=11;monthParser['Dec']=12;
          let startMonth = monthParser[monthString] - 1;*/
          let startMonth = parseInt(record.game_start_time.slice(5,7)) - 1;
          let startDay = parseInt(record.game_start_time.slice(8,10));
          //根据reserve、subscribe的情况为赛事添加用户类型，目前默认为Normal
          //record['u_type'] = 'Normal';
          if (value.month()==startMonth && value.date()==startDay) {
            listData.push(record)
        }
      }
      });
      console.log(listData);
      return listData;
    },
    
    showModal() {
      console.log(this.modal_visible);  
      this.modal_visible = true;
      console.log(this.modal_visible);
    },
    handleSubmit() {
      
    },
  },
};
</script>
<style scoped>
.box{
  margin: auto;
  width:1200px;
}
.events {
  list-style: none;
  margin: 0;
  padding: 0;
}
.events .ant-badge-status {
  overflow: hidden;
  white-space: nowrap;
  width: 100%;
  text-overflow: ellipsis;
  font-size: 12px;
}
.notes-month {
  text-align: center;
  font-size: 28px;
}
.notes-month section {
  font-size: 28px;
}

li {
  margin: 5px;
}


.Reserve{
  background-color: #ff3434;
  border-color: #ff3434;
}

.Subscribe{
  background-color:#2aa8ec;
  border-color: #2aa8ec;
}

.Normal{
  background-color:white;
  color: black;
}


.ant-badge{
  margin: 5px;
}

.switches {
  padding: 5px;
}

.badges span {
  margin-left: 5px;
  margin-right: 5px;
}

.badges::marker{
  content:'';
}
</style>
