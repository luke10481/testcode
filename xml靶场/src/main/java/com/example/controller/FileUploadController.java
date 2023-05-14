package com.example.controller;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import javax.xml.parsers.DocumentBuilderFactory;
import java.nio.charset.StandardCharsets;

@Controller
public class FileUploadController {

    @GetMapping("/")
    public String index() {
        return "upload";
    }

    @PostMapping("/upload")
    public String handleFileUpload(@RequestParam("file") MultipartFile file, Model model) {
        try {
            String content = new String(file.getBytes(), StandardCharsets.UTF_8);
            String parsedContent = parseInsecureXML(content);
            model.addAttribute("message", "File uploaded successfully.");
            model.addAttribute("parsedContent", parsedContent);
        } catch (Exception e) {
            e.printStackTrace();
            model.addAttribute("message", "Error processing file.");
        }
        return "upload";
    }

    private String parseInsecureXML(String content) throws DocumentException {
        Document document = DocumentHelper.parseText(content);
        Element root = document.getRootElement();
        return root.asXML();
    }

}