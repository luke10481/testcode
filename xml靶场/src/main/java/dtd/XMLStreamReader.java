package dtd;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import java.io.FileInputStream;


public class XMLStreamReader {

    public static void main(String[] args) {
        try {
            //System.out.println("用户的当前工作目录:/n"+System.getProperty("user.dir"));
            String xmlFile = "Data.xml";
            // Intentionally make the XMLInputFactory vulnerable to XXE
            XMLInputFactory factory = XMLInputFactory.newFactory();
            factory.setProperty(XMLInputFactory.SUPPORT_DTD, true);
            factory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, true);

            javax.xml.stream.XMLStreamReader reader = factory.createXMLStreamReader(new FileInputStream(xmlFile));

            while (reader.hasNext()) {
                int eventType = reader.next();

                if (eventType == XMLStreamConstants.START_ELEMENT && "content".equals(reader.getLocalName())) {
                    String content = reader.getElementText();
                    System.out.println("Extracted content: \n" + content);
                }
            }

            reader.close();
        }catch (Exception e){
            System.out.println(e);
        }
    }
}