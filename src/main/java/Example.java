import java.io.IOException;

import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.*;

@RestController
@EnableAutoConfiguration
public class Example {
	
	@Value("${HAT_COLOR:Red}")
	private String hatColor;

	@RequestMapping("/")
	public String home() {
		return "Hello " + hatColor + " Hat!!";
	}
		
    @RequestMapping(value = "/img", method = RequestMethod.GET, produces = MediaType.IMAGE_JPEG_VALUE)
    public void getImage(HttpServletResponse response) throws IOException {
    	ClassPathResource imgFile = null;
    	switch(hatColor) {
    	case "Yellow":
	    	imgFile = new ClassPathResource("image/yellowhat.jpeg");
    		break;
    	case "Red":
	    	imgFile = new ClassPathResource("image/redhat.jpeg");
	    	break;
    	}
    	if(imgFile != null) {
	    	response.setContentType(MediaType.IMAGE_JPEG_VALUE);
	        StreamUtils.copy(imgFile.getInputStream(), response.getOutputStream());
    	}
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(Example.class, args);
    }

}
