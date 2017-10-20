using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AttackSequence : MonoBehaviour {

    Quaternion originalRot;
    public GameObject tracker;
    float rotX, rotY, rotZ;
    public bool isAnim;

	//// Use this for initialization
	//void Start () {
 //       isAnim = true;
 //   }
	
	//// Update is called once per frame
	//void Update () {
 //       originalRot = Quaternion.Euler(new Vector3(tracker.transform.rotation.eulerAngles.x, tracker.transform.rotation.eulerAngles.y, tracker.transform.rotation.eulerAngles.z));
 //       rotX += Random.Range(0,5);
 //       rotY += Random.Range(0, 5);
 //       rotZ += Random.Range(0, 5);
 //       if (isAnim)
 //           gameObject.transform.rotation = Quaternion.Euler(new Vector3(tracker.transform.rotation.eulerAngles.x + rotX, tracker.transform.rotation.eulerAngles.y + rotY, tracker.transform.rotation.eulerAngles.z + rotZ));
 //       else
 //           gameObject.transform.rotation = originalRot;

 //       if (Input.GetKeyDown(KeyCode.Space))
 //           isAnim = !isAnim;
 //   }
}
