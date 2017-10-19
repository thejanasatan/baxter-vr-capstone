using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LookAtTarget : MonoBehaviour {

    public GameObject target;
    public Transform targetChildTransform;
    public Vector3 offset;
    public Vector3 rotOffset;
    public bool isRotating;
    public bool isFollowing;

    // Use this for initialization
    void Start () {
        isFollowing = true;
	}
	
	// Update is called once per frame
	void Update () {
        
        transform.LookAt(new Vector3(target.transform.position.x + offset.x, target.transform.position.y + offset.y, target.transform.position.z + offset.z));

        if (!isFollowing)
        {
            return;
        }

        if (gameObject.name == "Left Arm" || gameObject.name == "Left_Wrist_Joint_01")
        {
            targetChildTransform = target.transform.GetChild(0).GetChild(0);
            transform.LookAt(targetChildTransform);
        }
        else
        {
            //transform.LookAt(target.transform.position);
            transform.LookAt(new Vector3(target.transform.position.x + offset.x, target.transform.position.y + offset.y, target.transform.position.z + offset.z));
        }

        if (isRotating)
        {

            rotOffset = Vector3.zero;
            //rotOffset.x = -90;
            //rotOffset.y = -90;
            //rotOffset.z = -90;

            //if (target.transform.rotation.eulerAngles.z < 90 || target.transform.rotation.eulerAngles.z > 270)
            //{
            //    //print("Overturn");
            //    rotOffset.z = -180;
            //}

            transform.rotation = Quaternion.Euler(new Vector3(targetChildTransform.rotation.eulerAngles.x + rotOffset.x, targetChildTransform.rotation.eulerAngles.y + rotOffset.y, targetChildTransform.rotation.eulerAngles.z + rotOffset.z));

            //if (transform.rotation.eulerAngles.x < -50 && transform.rotation.eulerAngles.x > 90)
            //{
            //    transform.rotation = Quaternion.Euler(target.transform.rotation.eulerAngles.x - 180, target.transform.rotation.eulerAngles.y, target.transform.rotation.eulerAngles.z);
            //}
            //else
            //{
            //    //transform.rotation = target.transform.rotation;
            //    transform.rotation = Quaternion.Euler(new Vector3(-target.transform.rotation.eulerAngles.x - 90, 0, 0));
            //}

        }
    }
}
