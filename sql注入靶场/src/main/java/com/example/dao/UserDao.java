package com.example.dao;

import com.example.model.User;
import org.apache.ibatis.annotations.*;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper //表示这是Mybatis的mapper类
@Repository
public interface UserDao extends BaseMapper<User>{
    @Select("select * from user")
    List<User> queryUserList();
    @Select("select * from user where username = ${username}")
    List<User> queryUserByUsername(String username);
    @Insert("insert into user(id,username,password) values (#{id},#{username},#{password})")
    int addUser(User user);
    @Update("update user set username=#{username},password=#{password} where id=#{id}")
    int updateUser(User user);
    @Delete("delete from user where id=#{id}")
    int deleteUser(int id);
}