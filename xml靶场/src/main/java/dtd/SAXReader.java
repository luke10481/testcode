package dtd;

import org.dom4j.Document;
import org.dom4j.Element;
import java.io.File;

public class SAXReader {

    public static void main(String[] args) {
        try {
            String xmlFile = "Data.xml";
            org.dom4j.io.SAXReader reader = new org.dom4j.io.SAXReader();
            Document document = reader.read(new File(xmlFile));
            Element root = document.getRootElement();
            Element id = root.element("content");
            System.out.println("id: " + id.getTextTrim());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}