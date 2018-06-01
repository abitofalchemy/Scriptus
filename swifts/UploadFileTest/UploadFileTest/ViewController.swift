//
//  ViewController.swift
//  ImageUploadExample
//
//  Created by Sergey Kargopolov on 2015-03-07.
//  Copyright (c) 2015 Sergey Kargopolov. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
	
	@IBOutlet weak var myActivityIndicator: UIActivityIndicatorView!
	@IBOutlet weak var myImageView: UIImageView!
	
	@IBAction func uploadButtonTapped(sender: AnyObject) {
		
		myImageUploadRequest()
		
	}
	
	@IBAction func selectPhotoButtonTapped(sender: AnyObject) {
		
		let myPickerController = UIImagePickerController()
		myPickerController.delegate = self;
		myPickerController.sourceType = UIImagePickerControllerSourceType.photoLibrary
		
		self.present(myPickerController, animated: true, completion: nil)
		
	}
	
	
	
	internal func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any])
//		picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : AnyObject])
		
	{
		myImageView.image = info[UIImagePickerControllerOriginalImage] as? UIImage
		
		self.dismiss(animated: true, completion: nil)
		
	}
	
	
	
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
		
		//myImageUploadRequest()
		
	}
	
	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
		// Dispose of any resources that can be recreated.
	}
	
	
	
	
	
	
	func myImageUploadRequest()
	{
		
		let myUrl = NSURL(string: "http://10.0.0.40/uploadfile.php");
		//let myUrl = NSURL(string: "http://www.boredwear.com/utils/postImage.php");
		
		let request = NSMutableURLRequest(url:myUrl! as URL);
		request.httpMethod = "POST";
		
		let param = [
			"firstName"  : "sal",
			"lastName"    : "aguinaga",
			"userId"    : "9"
		]
		
		let boundary = generateBoundaryString()
		
		request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
		
		
		let imageData = UIImageJPEGRepresentation(myImageView.image!, 1)
		
		
		if(imageData==nil)  { return; }
		
		request.httpBody = createBodyWithParameters(parameters: param, filePathKey: "file", imageDataKey: imageData! as NSData, boundary: boundary) as Data
		
		
		
		myActivityIndicator.startAnimating();
		
		let task = URLSession.shared.dataTask(with: request as URLRequest) {
			data, response, error in
			
			if error != nil {
				print("error=\(String(describing: error))")
				return
			}
			
			// You can print out response object
			print("******* response = \(String(describing: response))")
			
			// Print out reponse body
			let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
			print("****** response data = \(responseString!)")
			
			do {
				let json = try JSONSerialization.jsonObject(with: data!, options: []) as? NSDictionary
				
				print(json!)
//				DispatchQueue.async(execute:)(dispatch_get_main_queue(),{
//					self.myActivityIndicator.stopAnimating()
//					self.myImageView.image = nil;
//				});

				DispatchQueue.main.async {
					self.myActivityIndicator.stopAnimating()
					self.myImageView.image = nil;
				}
			}catch
			{
				print(error)
			}
			
			
		}
		
		task.resume()
		
	}
	
	
	func createBodyWithParameters(parameters: [String: String]?, filePathKey: String?, imageDataKey: NSData, boundary: String) -> NSData {
		let body = NSMutableData();
		
		if parameters != nil {
			for (key, value) in parameters! {
				body.appendString(string: "--\(boundary)\r\n")
				body.appendString(string: "Content-Disposition: form-data; name=\"\(key)\"\r\n\r\n")
				body.appendString(string: "\(value)\r\n")
			}
		}
		
		let filename = "user-profile.jpg"
		
		let mimetype = "image/jpg"
		
		body.appendString(string: "--\(boundary)\r\n")
		body.appendString(string: "Content-Disposition: form-data; name=\"\(filePathKey!)\"; filename=\"\(filename)\"\r\n")
		body.appendString(string: "Content-Type: \(mimetype)\r\n\r\n")
		body.append(imageDataKey as Data)
		body.appendString(string: "\r\n")
		
		
		
		body.appendString(string: "--\(boundary)--\r\n")
		
		return body
	}
	
	
	
	
	func generateBoundaryString() -> String {
		return "Boundary-\(NSUUID().uuidString)"
	}
	
	
	
}



extension NSMutableData {
	
	func appendString(string: String) {
		let data = string.data(using: String.Encoding.utf8, allowLossyConversion: true)
		append(data!)
	}
}
