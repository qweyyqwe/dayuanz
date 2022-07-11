<<<<<<< HEAD
<template>
  <div>
    11111111111111111111
    <span>第{{ days }}天</span>
    <!-- <p class="history" @click="goToHistory">View score history</p> -->
    <ul class="signBtnBox">
      <!-- <li v-for="data in list1"> -->
      <li v-for="data in list1" :key="data.index">
        1111111111111???{{data.id}}————{{data.index}}
        <div
          v-if="Number(days) == data.id  || Number(days) > data.id "
          style="
            width: 100%;
            height: 100%;
            border-radius: 4px;
            background-color: #ff9400;
          "
        >
          <img src="static/img/money.png" style="width: 100px; height: 100px" />

          <p>{{ data.days }}</p>
        </div>
        <div v-else @click="signInToday" style="cursor:pointer">
          <img
            src="static/img/qiandao.png"
            style="width: 100px; height: 100px"
          />

          <p>{{ data.days }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      list1: [],
            list2: [
        { id: 1, days: 1 },
        { id: 2, days: 2 },
        { id: 3, days: 3 },
        { id: 4, days: 4 },
        { id: 5, days: 5 },
        { id: 6, days: 6 },
        { id: 7, days: 7 },
      ],
      res: "",
      /* 签到的总天数 */
      days: '',
      signOK: "",
    };
  },
  methods: {
    goToHistory() {
      this.$openUrl(assetsVersionDir + "index.html?#/profile/wallet/points", 1);
    },
    // 获取奖励列表赋值给list1
    allReward() {
      this.axios.get("sign_in/reward_list/").then((res) => {
        if (res.data.code == 200) {
          this.list1 = res.data.data;
        }
      });
    },
    // signInToday() {
    //   // console.log(this.res.data.today);
    //   if (this.res.data.today == 0) {
    //     this.todaySignIn();
    //     console.log(this.res.code);
    //     if (this.res.code !== 0) {
    //       this.$message.success("签到失败");
    //     } else {
    //       this.$message.error("签到成功");
    //     }
    //   } else {
    //     this.$message.error("今日已签到");
    //   }
    // },
        signInToday() {
      this.axios.post("sign_in/sign/").then((res) => {
        if (res.data.code == 200) {
          alert(res.data.msg);
          // this.btnChangeEnable = true;
          this.getStatus();
          this.starttime = res.data.start_time;
        } else {
          alert(res.data.msg);
        }
      });
    },
  },
  mounted() {
    this.allReward();
  },
};
</script>

<style>
=======
<template>
  <div>
    11111111111111111111
    <span>第{{ days }}天</span>
    <!-- <p class="history" @click="goToHistory">View score history</p> -->
    <ul class="signBtnBox">
      <!-- <li v-for="data in list1"> -->
      <li v-for="data in list1" :key="data.index">
        1111111111111???{{data.id}}————{{data.index}}
        <div
          v-if="Number(days) == data.id  || Number(days) > data.id "
          style="
            width: 100%;
            height: 100%;
            border-radius: 4px;
            background-color: #ff9400;
          "
        >
          <img src="static/img/money.png" style="width: 100px; height: 100px" />

          <p>{{ data.days }}</p>
        </div>
        <div v-else @click="signInToday" style="cursor:pointer">
          <img
            src="static/img/qiandao.png"
            style="width: 100px; height: 100px"
          />

          <p>{{ data.days }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      list1: [],
            list2: [
        { id: 1, days: 1 },
        { id: 2, days: 2 },
        { id: 3, days: 3 },
        { id: 4, days: 4 },
        { id: 5, days: 5 },
        { id: 6, days: 6 },
        { id: 7, days: 7 },
      ],
      res: "",
      /* 签到的总天数 */
      days: '',
      signOK: "",
    };
  },
  methods: {
    goToHistory() {
      this.$openUrl(assetsVersionDir + "index.html?#/profile/wallet/points", 1);
    },
    // 获取奖励列表赋值给list1
    allReward() {
      this.axios.get("sign_in/reward_list/").then((res) => {
        if (res.data.code == 200) {
          this.list1 = res.data.data;
        }
      });
    },
    // signInToday() {
    //   // console.log(this.res.data.today);
    //   if (this.res.data.today == 0) {
    //     this.todaySignIn();
    //     console.log(this.res.code);
    //     if (this.res.code !== 0) {
    //       this.$message.success("签到失败");
    //     } else {
    //       this.$message.error("签到成功");
    //     }
    //   } else {
    //     this.$message.error("今日已签到");
    //   }
    // },
        signInToday() {
      this.axios.post("sign_in/sign/").then((res) => {
        if (res.data.code == 200) {
          alert(res.data.msg);
          // this.btnChangeEnable = true;
          this.getStatus();
          this.starttime = res.data.start_time;
        } else {
          alert(res.data.msg);
        }
      });
    },
  },
  mounted() {
    this.allReward();
  },
};
</script>

<style>
>>>>>>> 74dfda3f4b992f39b4b31476d3023624a6535a86
</style>