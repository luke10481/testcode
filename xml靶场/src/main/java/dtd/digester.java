package dtd;

import org.apache.commons.digester3.Digester;
import org.apache.commons.digester3.Rule;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.IOException;

public class digester {

    public static void main(String[] args) {
        try {
            String xmlFile = "Data.xml";
            Digester digester = new Digester();
            digester.setValidating(false);

            StringBuilder idBuilder = new StringBuilder();
            digester.addRule("data/content", new Rule() {
                @Override
                public void body(String namespace, String name, String text) throws SAXException {
                    idBuilder.append(text);
                }
            });

            digester.parse(new File(xmlFile));

            System.out.println("id: " + idBuilder.toString());
        } catch (IOException | SAXException e) {
            System.out.println(e);
        }
    }
}