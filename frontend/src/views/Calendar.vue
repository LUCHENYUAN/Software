<template>
  <div class="box">
    <li><h1>赛事日历</h1></li>
    <li class="badges">
      <span class="preferChoice">
        筛选设置：
      <a-badge color="#ff3434" text="已预约"/>
      <a-switch default-checked @change="onChangeReserve"></a-switch>
      <a-badge color="#2aa8ec" text="已订阅"/>
      <a-switch default-checked @change="onChangeSubscribe"></a-switch>
      <a-badge color="#993399" text="推荐赛事"/>
      <a-switch default-checked @change="onChangeRecommend"></a-switch>
      <a-badge color="white" text="其他可用赛事"/>
      <a-switch default-checked @change="onChangeNormal"></a-switch>
      </span>
    </li>
    <li>
      <span class="lengthChoice">
        比赛时长：
        <a-select default-value="all" style="width: 120px" @change="handleChangeLength">
          <a-select-option value="all">
          所有
          </a-select-option>
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
        <a-select default-value="all" style="width: 120px" @change="handleChangeDiff">
          <a-select-option value="all">
          所有
          </a-select-option>
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
      <div v-for="item in getListData(value)" :key="item.game_id">
      <li v-if="item.cust_public==1 || item.cust_user_id==token">
        <a-popover :title=item.game_name trigger="click" placement="bottomLeft">
        <template slot="content"> 
          <p v-if="item.platform">平台：{{item.platform}}</p>
          <p>开始时间：{{item.game_start_time}}</p>
          <p v-if="item.game_end_time">结束时间：{{item.game_end_time}}</p>
          <p v-if="item.duration">时长：{{item.duration}}</p>
          <span>
            <p>链接：<a :href=item.website>{{item.website}}</a></p>
          </span>
          <a v-if="item.u_type != 'Reserve'" @click="ReserveGame(item.game_id)" style="font-weight:bold">预约</a>
          <a v-if="item.u_type == 'Reserve'" @click="ReserveGameCancel(item.game_id)" style="font-weight:bold" >取消预约</a>
        </template>
        <a-button :class=item.u_type type="primary">
          {{item.game_name}}
        </a-button>
        </a-popover>
      </li>
      </div>
    </ul>
    <!--
    <template slot="monthCellRender" slot-scope="value">
      <div v-if="getMonthData(value)" class="notes-month">
        <section>{{ getMonthData(value) }}</section>
        <span>Backlog number</span>
      </div>
    </template>--->
  </a-calendar>

  <li class="badges"><h1>我的自定义赛事</h1></li>

  <a-button type="primary" @click="showModal">
      上传自定义赛事
    </a-button><br/><br/>

    <a-modal v-model="modal_visible" title="填写自定义赛事信息" @ok="handleSubmit()" :destroyOnClose="true">
      <a-form :form="new_cust_form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }">
    <a-form-item label="比赛名称">
      <a-input
        v-decorator="['cust_game_name', { rules: [{ required: true, message: '请输入比赛名称！'}] }]"
      />
    </a-form-item>
    <a-form-item label="起止时间">
      <a-range-picker
        :disabled-date="disabledDate"
        :disabled-time="disabledRangeTime"
        :show-time="{
          hideDisabledOptions: true,
          defaultValue: [moment('00:00:00', 'HH:mm:ss'), moment('11:59:59', 'HH:mm:ss')]
        }"
        format="YYYY-MM-DD HH:mm:ss"
        v-decorator="['cust_game_time', { rules: [{ required: true, message: '请输入起止时间！'}] }]"
      />
    </a-form-item>
    <a-form-item label="比赛链接">
      <a-input
        v-decorator="['cust_game_website', { rules: [{ required: true, message: '请输入比赛链接！'}] }]"
      />
    </a-form-item>
    <a-form-item label="举办方">
      <a-input
        v-decorator="['cust_game_platform', { rules: [{ required: true, message: '请输入举办方！'}] }]"
      />
    </a-form-item>
    <a-form-item label="是否公开">
      <a-switch default-checked v-decorator="['cust_public', { rules: [{ required: true}] }]"></a-switch>
    </a-form-item>
    </a-form>
    </a-modal>

  <a-table rowKey="game_id" :columns="tableColumns" :data-source="this.cust_matches">
    <span slot="website" slot-scope="text"><a :href="text">{{ text }}</a></span>
    <span slot="public" slot-scope="text">{{ text ? '公开' : '私密' }}</span>
    <span slot="action" slot-scope="text, record">
      <a v-if="record.cust_public == 1" @click="privateCusGame(record.game_id)">设为私密</a>
      <a v-if="record.cust_public == 0" @click="publicCusGame(record.game_id)">设为公开</a>
      <a-divider type="vertical"/>
      <a @click="deleteCusGame(record.game_id)">删除</a>
    </span>
  </a-table>

    
  </div>
</template>

<script>
import moment from 'moment';
import Vue from 'vue'

//自定义比赛信息表
const tableColumns = [
  {
    title: '比赛名',
    dataIndex: 'game_name',
    key: 'game_name',
    width: '20%',
    
  },
  {
    title: '开始时间',
    dataIndex: 'game_start_time',
    key: 'game_start_time',
    width: '15%',
  },
  {
    title: '结束时间',
    dataIndex: 'game_end_time',
    key: 'game_end_time',
    width: '15%',
  },
  {
    title: '比赛链接',
    dataIndex: 'website',
    key: 'website',
    width: '20%',
    scopedSlots: { customRender: 'website' },
  },
  {
    title: '举办方',
    key: 'platform',
    width: '10%',
  },
  {
    title: '公开状态',
    dataIndex: 'cust_public',
    key: 'cust_public',
    width: '5%',
    scopedSlots: { customRender: 'public' },
  },
  {
    title: '操作',
    key: 'action',
    width: '15%',
    scopedSlots: { customRender: 'action' },
  },
]

export default {
  data() {
    return {
      token: '',
      needType: ['Reserve', 'Subscribe', 'Normal', 'Recommend'],
      matches:[],
      cust_matches:[],
      subscribes:[],
      reserves:[],
      visible: false,
      modal_visible: false,
      condition_duration: 'all',
      condition_level: "all",
      tableColumns,
      new_cust_form: this.$form.createForm(this,{name: 'new_game'}),
    }
  },
  //挂载阶段获取预约、订阅、比赛信息
  mounted:function(){
      //debug，输出当前用户名，从sessionStroage里拿
      this.token = sessionStorage.getItem('token');
      
      let reserveUrl = "http://127.0.0.1:5000/reserve/";
      reserveUrl += `${this.token}`;
      //获取当前用户的预约信息
      Vue.axios.get(reserveUrl).then((response)=>{
        this.reserves=response.data;
        
      }).catch((response)=>{
        console.log(response);
      });

      //获取当前用户的订阅信息
      let subscribeUrl = "http://127.0.0.1:5000/subscribe/";
      subscribeUrl += `${this.token}`;
      Vue.axios.get(subscribeUrl).then((response)=>{
        this.subscribes=response.data['platform'].split(',');
      }).catch((response)=>{
        console.log(response); 
      });

      //获取推荐信息
      //???

      //获取全部比赛信息接口
      Vue.axios.get('http://127.0.0.1:5000/game/all').then((response)=>{
        this.matches=response.data;
        //添加预约、订阅、推荐、其他标签
        for (var record of this.matches) {
          record['u_type'] = 'Normal';

          if (this.reserves.indexOf(record.game_id)!=-1) {
            record['u_type'] = 'Reserve';
          }
          else if (this.subscribes.indexOf(record.platform)!=-1) {
            record['u_type'] = 'Subscribe';
          }
          /*else if (this.recommend.indedxOf(record.???)!=-1) {
            record['u_type'] = 'Recommend';
          }*/

          //自定义赛事单独拿出
          if (record.cust_user_id == this.token) {
            this.cust_matches.push(record);
          }
        }
      }).catch((response)=>{
        console.log(response);
      });
      /*

     /*mock测试端口
     Vue.axios.get('http://127.0.0.1:4523/mock/1025901/reserve/id').then((response)=>{
        this.reserves=response.data;
        console.log(this.reserves);
      }).catch((response)=>{
        console.log(response);
      });
      */
    },
    updated(){
      console.log("Re-rendered.")
    },
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
    onChangeRecommend() {
      let label = this.needType.indexOf('Recommend');
      if (label != -1) {
        this.needType.splice(label, 1);
        console.log('Recommend Deleted from needType!');
        console.log(this.needType);
      }
      else {
        this.needType.push('Recommend');
        console.log('Recommend Added to needType!');
        console.log(this.needType);
      }
    },
    ReserveGame(game_id){
        this.matches[game_id-1].u_type='Reserve';
        /*想办法解决卡片颜色和预约按钮更新的问题*/
        Vue.axios.post("http://127.0.0.1:5000/reserve/add",{
        token: this.token,
        reserve_game_id: game_id,
        }).then((res)=>{
          console.log(res.data.info)
        }).catch((res)=>{
          console.log(res)
        })
    }, 
    ReserveGameCancel(game_id) {
      console.log(this.matches[game_id-1].u_type);
      this.matches[game_id-1].u_type='Normal';
      console.log(this.matches[game_id-1].u_type);
       Vue.axios.post("http://127.0.0.1:5000/reserve/delete",{
        token: this.token,
        reserve_game_id: game_id,
        }).then((res)=>{
          console.log(res.data.info)
        }).catch((res)=>{
          console.log(res)
        }) 
    },
    handleChangeDiff() {
      
    },
    handleChangeLength() {

    },
    //日历格渲染函数
    getListData(value) {
      let listData = [];
      let ReserveData = [];
      let SubscribeData =[];
      let OtherData = [];
      for (var record of this.matches) {
      //接口月份转换
      let monthString = record.game_start_time.slice(8,11);
      var monthParser = new Array();
      monthParser['Jan']=1;monthParser['Feb']=2;monthParser['Mar']=3;monthParser['Apr']=4;monthParser['May']=5;monthParser['Jun']=6;
      monthParser['Jul']=7;monthParser['Aug']=8;monthParser['Sep']=9;monthParser['Oct']=10;monthParser['Nov']=11;monthParser['Dec']=12;
      let startMonth = monthParser[monthString] - 1;
      let startDay = parseInt(record.game_start_time.slice(5,7));

      //排序要渲染的赛事，从上到下先后为预约、订阅、推荐、其他
      if (value.month()==startMonth && value.date()==startDay && this.needType.indexOf(record['u_type'])!=-1) {
        if (record['u_type']==='Reserve') {
          ReserveData.push(record);
        }
        else if (record['u_type']==='Subscribe') {
          SubscribeData.push(record);
        }
        else {
          OtherData.push(record)
        }
      }
      }
      console.log(listData);
      listData = listData.concat(ReserveData);
      listData = listData.concat(SubscribeData);
      listData = listData.concat(OtherData);
      return listData;
    },
    
    showModal() {
      console.log(this.modal_visible);  
      this.modal_visible = true;
      console.log(this.modal_visible);
    },
    range(start, end) {
      const result = [];
      for (let i = start; i < end; i++) {
        result.push(i);
      }
      return result;
    },
    disabledDate(current) {
      return current && current < moment().endOf('day');
    },
    disabledRangeTime() {
      return;
    },
    privateCusGame(game_id) {
      /*设置公开与私密的即时渲染还没完成*/
      Vue.axios.post("http://127.0.0.1:5000/game/update_public",{
        token: this.token,
        game_id: game_id,
        new_public: 0,
        }).then((res)=>{
          console.log(res.data.info)
        }).catch((res)=>{
          console.log(res)
        })
    },
    publicCusGame(game_id) {

      Vue.axios.post("http://127.0.0.1:5000/game/update_public",{
        token: this.token,
        game_id: game_id,
        new_public: 1,
        }).then((res)=>{
          console.log(res.data.info)
        }).catch((res)=>{
          console.log(res)
        })
    },
    deleteCusGame(game_id) {
      Vue.axios.post("http://127.0.0.1:5000/game/delete_custom_game", {
        token: this.token,
        game_id: game_id,
      }).then((res)=>{
        console.log(res.data.info)
      }).catch((res)=>{
        console.log(res)
      })
    },
    handleSubmit() {
      this.new_cust_form.validateFields((err, values) => {
        if (!err) {
        Vue.axios.post("http://127.0.0.1:5000/game/add_custom_game", {
          token: this.token,
          cust_game_info: values,
        }).then((res)=>{
          console.log(res.data.info)
        }).catch((res)=>{
          console.log(res)
        });
        const TIME_COUNT = 2;
        const hide = this.$message.loading('添加成功！即将返回赛事页！', 0);
        setTimeout(hide, 2500);
        if(!this.timer){
            this.count = TIME_COUNT;
            this.show = false;
            this.timer = setInterval(()=>{
            if(this.count > 0 && this.count <= TIME_COUNT){
                this.count--;
            }else{
                this.show = true;
                clearInterval(this.timer);
                this.timer = null;
                //跳转的页面写在此处
                this.modal_visible=false;
            }
          },1000)
        }
        }
      });
      this.new_cust_form.clearField();
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

.Recommend{
  background-color: #993399;
  border-color: #993399;
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

li::marker{
  content:'';
}
</style>
