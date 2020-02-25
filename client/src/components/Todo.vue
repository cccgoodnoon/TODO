<template>
  <div id="main">
    <!-- header 头部 -->
    <div class="g-header">
      <h1>Todos</h1>
      <div class="f-add">
        <span class="switch" v-show="todoList.length>0" @click="selectAllTodos"></span>
        <input type="text"
              class="f-add-task"
              placeholder="What needs to be done?"
              autofocus
        >
        <button type="button" class="f-add-button addBtn" @click="isShow = true;isAdd=true;isEdit=false;">添加</button>
        
      </div>
    </div>
    <div class="addModel" v-if="isShow">
      <div><span>描述：</span><textarea v-model="description" ></textarea></div>
      <div v-if="isAdd"><span>开始时间：</span><input v-model="begintime" type="date"> </div>
      <div v-if="isAdd"><span>结束时间：</span><input v-model="endtime" type="date"></div>
      <div v-if="isEdit"><span>开始时间：</span><input v-model="begintime1" type="text"> </div>
      <div v-if="isEdit"><span>结束时间：</span><input v-model="endtime1" type="text"></div>
      <input v-model="state" type="hidden"><br>
      <button type="button" class="f-add-button addBtn closeBtn" @click="isShow = false;">取消</button>
      <button type="button" class="f-add-button addBtn saveBtn" @click="addTodo">保存</button>
    </div>
    <!-- 任务 -->
    <section class="g-content">
      <table class="listTB">
        <tr v-for="(todo,index) in todoList" :key=index >
            <td>
              <span v-if="todo.state == '2'">
                <input type="checkbox" class="u-check" @click="toChecked(todo,index)" v-model="todo.isChecked">
              </span>
             <span v-if="todo.state == '9'">
                <input type="checkbox" class="u-check" checked disabled v-model="todo.isChecked">
              </span>
            </td>
            <td>
              <span v-if="todo.state == '2'">
                <div  v-show="!todo.status" @dblclick="toEdit(todo)" :class="{f_delete:todo.isChecked}" style="font-size:17px;float:left;"> 
                  {{todo.description}}
                </div>
              </span>
              <span v-if="todo.state == '9'">
              <div  v-show="!todo.status" @dblclick="toEdit(todo)" class="f_delete" style="font-size:17px;float:left;"> 
                  {{todo.description}}
                </div>
              </span>
              
            </td>
            <td style="width:150px;">
              <span class="editBtn"
                    @click="editTodo(todo)"
                    title="修改"
              ><img src="../assets/edit.png" width="25px"></span>
              
              <span style="margin-left:20px;"  class="delBtn"
                    @click="deleteTodo(todo)"
                    title="删除"
              ><img src="../assets/delete.png" width="25px"></span>
            </td>
        </tr>
      </table>
      <!-- 底部按钮 -->
      <div class="g-footer-btn">
        <!-- <span class="g-data-num">{{countCompletedNum}} item left</span> -->
        <ul class="filters">
          <li>
            <a href="javascript:;"  @click="getAll">All</a>
          </li>
          <li>
            <a href="javascript:;"  @click="getByState(2)">Activing</a>
           </li>
          <li>
            <a href="javascript:;" @click="getByState(9)">Completed</a>
          </li>
        </ul>
        <div >
          <!-- <a href="#" class="clear-completed" @click="deleteAllCompleted">清空已完成</a> -->
        </div>
      </div><br><br>
    </section>
    <!-- /content 内容区-->
  </div>
</template>

<script>

import {getAllTask, addTask, deleteTask, updateTask, updateManyTask, deleteCompletedTask} from '../../api/api.js'

let filters = {
  isAll: function (todos) {
    return todos
  },
  isActiving: function (todos) {
    return todos.filter(function (todo) {
      return !todo.isChecked
    })
  },
  isChecked: function (todos) {
    return todos.filter(function (todo) {
      return todo.isChecked
    })
  }
}

export default {
  name: 'Todo',
  data: function () {
    return {
      todoList: [],
      isChecked: false,
      visibility: 'isAll',
      description:'',
      begintime:'',
      endtime:'',
      begintime1:'',
      endtime1:'',
      state:'2',
      isShow:false,
      isAdd:false,
      isEdit:false,
      id:"",
    }
  },
  computed: {
    // 使用计算属性计算所有未完成todos的次数
    // countActivingNum () {
    //   return filters.isActiving(this.todoList).length
    // },
    // // 计算已完成的个数
    // countCompletedNum () {
    //   return this.todoList.length - this.countActivingNum
    // }
  },
  mounted(){

  },  
  methods: {
     //根据状态查询
    getByState(state){
      var thiz = this;
      this.axios.get('/api/rest/anon/tasks/getByState/'+state)
      .then(msg =>{
        console.log(msg,88888)

          thiz.todoList = msg.data;
        
      })
    },
    //保存
    addTodo(){
        var thiz = this;
        //添加
        if(this.isAdd){
          this.axios.post('/api/rest/anon/tasks/add/'+this.begintime+"/"+this.endtime+"/"+this.description+"/"+this.state)
          .then(msg =>{
              console.log(msg)
              this.$message.success('添加成功!');
              thiz.getAll();
              thiz.isShow = false;
          })
        }
        //修改
        if(this.isEdit){
          this.axios.post('/api/rest/anon/tasks/edit/'+this.begintime1+"/"
            +this.endtime1+"/"+this.description+"/"+this.state+"/"+this.id)
          .then(msg =>{
              console.log(msg)
              this.$message.success('编辑成功!');
              thiz.getAll();
              thiz.isShow = false;
          })
        }
    },
    //修改
    editTodo(row){
        this.isShow = true;
        this.isAdd=false;
        this.isEdit=true;
        this.description = row.description;
        this.begintime1 = row.begintime.substring(0,10);
        this.endtime1 = row.endtime.substring(0,10);
        this.state = row.state;
        this.id = row.id;
        
    },
    // 设置todo的状态
    toChecked (todo, index) {
      if(todo.state == 9){
        // alert("该任务已经完成！")
        this.$message.success('该任务完成！');

        return false;
      }
      // console.log('已完成？' + index)
      var thiz = this;
      this.axios.post('/api/rest/anon/tasks/editState/9/'+todo.id)
        .then(msg =>{
            console.log(msg)
            this.$message.success('该任务完成！');
            thiz.getAll();
        })
    },
    //删除操作
    deleteTodo(val){
      var thiz = this;
      this.$confirm('确定删除吗', '提示', {
        type: 'warning'
      }).then(() => {
          this.axios.get('/api/rest/anon/tasks/delete/'+val.id).then(res => {
              this.$message.success('删除成功!');
              thiz.getAll(); 
          }).catch((res) => {
              this.$message.error('删除失败!');
          });
      }).catch(() => {
          this.$message.info('已取消操作!');
      });

    },
    // 过滤任务列表
    filteredTodoList () {
      return filters[this.visibility](this.todoList)
    },
    // 判断当前的todo是否属于filteredTodoList
    isShowFilted (todo) {
      return this.filteredTodoList().some(function (item) {
        return item._id === todo._id
      })
    },

    getAll: function () {
      let _this = this
      this.axios.get('/api/rest/anon/tasks')
      .then(res => {
        if (res.status === 200) {
          _this.todoList = res.data
          console.log(_this.todoList)
        } else {
          alert('信息获取失败，请查看服务器是否开启')
        }
      })
    },
    // 全选功能
    selectAllTodos: function () {
      let _this = this
      let isChecked = !_this.todoList.every((todo) => todo.isChecked)
      updateManyTask({isChecked: isChecked}).then(data => {
        if (data.code === 0) {
          _this.getAll()
        }
      })
    },   
    // 批量删除已完成任务
    deleteAllCompleted () {
      let _this = this
      let idString = _this.todoList.filter(todo => todo.isChecked).map(todo => {
        let id = todo.id || todo._id
        return id
      }).join(',')
      deleteCompletedTask({ids: idString}).then(data => {
        _this.getAll()
      })
    },
    toEdit (item) {
      item.status = true
    },
    // 修改任务
    unEdit (item) {
      item.status = false
      this.toChecked(item, false)
    }
  },
  // 自定义focus指令
  directives: {
    'todo-focus': function (el, binding) {
      if (binding.value) {
        el.focus()
      }
    }
  },
  created () {
    this.getAll()
  }
}
</script>

<style>
#main{
  padding:100px 0;
  margin:0 auto;
  width:600px;
  height:100%;
  text-align: center;
  /* border: 1px black solid; */
}

#main .g-header{
  width: 100%;
  color: rgba(175,47,47,.15);
  text-rendering: optimizeLegibility; /*浏览器强调了渲染速度和几何精度的可读性。这样可以进行字距调整和可选的连字。*/
  /* border: 2px green solid; */
}

#main .g-header h1{
  font-size: 100px;
  font-weight: 100;
}

#main .g-header .f-add{
  position: relative;
  margin: 10px 0 0;
  /* border: 1px red solid; */
}
#main .g-header .f-add .switch{
  width: 26px;
  height: 26px;
  background:url('../assets/icon-down-eee.png') center center no-repeat;
  position: absolute;
  top: 18px;
  
  left: 22px;
  /* cursor: pointer; */
}

#main .g-header .f-add .f-add-task{
  padding: 16px 16px 16px 65px;
  border: none;
  box-sizing: border-box;
  box-shadow: inset 0 -2px 1px rgba(222, 222, 222, 0.03);
  width: 100%;
  font-size: 24px;
  color: #000;
  font-weight: inherit;
}

#main .g-header .f-add .f-add-button{
  position: absolute;
  width: 80px;
  height: 80px;
  line-height: 20px;
  top: 10px;
  right: 10px;
  cursor: pointer;
  outline:none;
}

/* content */
#main .g-content{
  position: relative;
  margin: 0 auto;
  width: 100%;
  box-shadow: 0 3px 3px 2px rgba(0, 0, 0, 0.25);
}

#main .g-content .g-tasklist{
  position: relative;
  z-index: 6;
}

#main .g-content .g-tasklist .m-tasks{
  display: flex;
  flex-direction: row;
  font-size:24px;
  padding:8px;
  background: #fff;
  align-items: center;
  /* border: 1px red solid; */
}

#main .g-content .g-tasklist .m-tasks:hover{
  background-color: #ccc;
}

#main .g-content .g-tasklist .m-tasks .u-check{
  width: 24px;
  height: 24px;
  margin-left: 12px;
  /* border: 1px red solid; */
}

.u-close-icon{
  background:url('../assets/delete.png') no-repeat;
  background-size: 100%;
}

#main .g-content .g-tasklist .m-tasks:hover .u-close{
  position: absolute;
  right: 1rem;
  cursor: pointer;
  width: 1.5rem;
  height: 1.5rem;
  display: block;
}

.u-message{
  flex:1;
  text-align: left;
  margin-left: 16px;
  font-size: 20px;
  padding: 6px 0;
  word-break: break-all;
  display: block;
  line-height: 1.2;
  transition: color 0.4s;
}

.u-update{
  position: relative;
  z-index:1;
}

.g-footer-btn{
  display: flex;
  justify-content: space-between;
  padding: .1rem;
  font-size: 16px;
  font-weight: 300;
  color: rgb(145, 145, 145);
}

.g-footer-btn .g-data-num{
  margin-left: 10px;
  /* background-color: red; */
}

.filters{
  margin: 0;
  padding: 0;
  list-style: none;
  position: absolute;
  right: 0;
  left: 0;
}

.filters li{
  display: inline;
}

.filters li a{
  color: inherit;
  margin: 3px;
  padding: 3px 7px;
  text-decoration: none;
  border: 1px solid transparent;
  border-radius: 12px;
}

.filters li a:hover{
  border-color: rgba(175, 47, 47, 0.1);
  /* background: rgba(175, 47, 47, 0.2); */

}

.filters li a:focus{
  background: rgba(175, 47, 47, 0.2);

}

/* .filters li a.selected{
  border-color: rgba(175, 47, 47, 0.2);
} */

.f_delete{
  text-decoration: line-through;
  color: #bbb;
}

.clear-completed{
  position: relative;
  width: 2.3rem;
}

.clear-completed:hover {
  cursor: pointer;
  /* text-decoration: underline; */
}
.addBtn{
    border: none;
    background: #71c9ce;
    height: 40px !important;
    border-radius: 18px;
    font-size: 15px;
    color: #fff;
    width:80px;
    
}
.addModel{
    width: 400px;
    height: 300px;
    /* border: 1px solid #666; */
    padding:20px;
    background: #fff;
    border-radius: 5px;
    position: fixed;
    z-index: 10000000000;
    left: 36%;
    box-shadow: gray 5px 10px 20px 5px ;
}
.addModel input,.addModel textarea{
  width:250px;
  margin-top:15px;
  margin-left:15px;

  border-radius: 5px;
}
.addModel span{
  width:100px;
}
.addModel input{
  height: 35px;
  border: 1px solid #bfbdbd;
  padding-left: 10px;
}
.addModel textarea{
  height: 60px;
}

.closeBtn{
  background:#ddd;
  color:#333;
  margin-right: 10px;
  cursor: pointer;
  outline:none;

}

.saveBtn{
  cursor: pointer;
  outline:none;

}
.listTB{
  width:100%;
  font-size: 15px;
}
.listTB tr{
  height: 40px;
}

.listTB input{
  height: 20px;
  width:20px;
}
.editBtn{
  color:blue;
  cursor: pointer;
}
.editBtn:hover{
  color:#060694;
}
.delBtn{
  color:red;
  cursor: pointer;
}
.delBtn:hover{
  color:#b90404;
}
</style>
