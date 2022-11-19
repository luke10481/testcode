package com.example.controller;

import com.example.dao.UserDao;
import com.example.model.User;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.metadata.OrderItem;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@RestController
public class UserController {
    @Autowired
    private UserDao userMapper;

    @GetMapping("/queryUserList")
    public List<User> queryUserList() {
        List<User> users = userMapper.queryUserList();
        return users;
    }

    @GetMapping("/queryUserByUsername{username}")
    public List<User> queryUserByUsername(String username) {
        List<User> users = userMapper.queryUserByUsername(username);
        return users;
    }

    @GetMapping("/addUser")
    public String addUser() {
        userMapper.addUser(new User(4, "zml", "45632"));
        return "增加用户完毕";
    }

    @GetMapping("/updateUser")
    public String updateUser() {
        userMapper.updateUser(new User(4, "zml", "678910"));
        return "修改用户完毕";
    }

    @GetMapping("/deleteUser")
    public String deleteUser() {
        userMapper.deleteUser(4);
        return "删除用户完毕";
    }

    @RequestMapping("/selectpage")
    public List<User> selectPage(Long page,Long size,String order){

        QueryWrapper<User> qw = new QueryWrapper<>();
        Page<User> personPage = new Page<>(page,size);
        personPage.addOrder(OrderItem.asc(order));
        IPage<User> iPage = userMapper.selectPage(personPage, qw);
        List<User> persons = iPage.getRecords();
        return persons;
    }
}