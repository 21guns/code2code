package ${package_name}.${module_name};

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;


@Configuration
@EnableScheduling
@EnableAutoConfiguration
@ComponentScan(basePackages = {"com.guns21", "com.ktjr"},
		excludeFilters = {@ComponentScan.Filter(classes = {SpringBootApplication.class})})
@MapperScan("com.ktjr.**.mapper")
public class AdminApplication {

	public static void main(String[] args) {

		SpringApplication.run(AdminApplication.class, args);
	}
}
