public class Crawler{

	String[] getAllUrls(String htmlContent);

	void appendDownloadedUrl(String url);

	void appendErrorUrl(String url);

	boolean isDownloaded(String url);

	String getPageContent(String url) throws CrawlException, IOException;

	String savePageContent(String pageContent);

	String rootNode;

	final static int WIDTH = 50;
	final static int HEIGHT = 5;


	void crawl(String url, level){
		try{
			String pageContent = getPageContent(url);
		} catch( Exception e ){
			appendErrorUrl(url);
			return;
		}

		savePageContent(pageContent);

		if ( level == HEIGHT )
			return;

		String[] urls = getAllUrls(pageContent);

		for( int i = 0; i < urls.length; i ++ ){

			if ( i == WIDTH )
				return;
			if ( isDownloaded(urls[i]))
				continue;
			crawl( urls[i], level + 1 );
		}
	}

	start(){
		crawl("http://www.mafengwo.com.cn", 0 );
	}

}