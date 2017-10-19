using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BaxterModel : MonoBehaviour {

    public GameObject targetFollow;
    public GameObject lookAt;
    Animator anim;
    Vector3 prevLoc = Vector3.zero;
    public bool isShooter;
    //public float damping;

    // Use this for initialization
    void Start () {
        //animation = GetComponent<Animation>();
        if (!isShooter)
            anim = GetComponent<Animator>();
	}
	
	// Update is called once per frame
	void Update () {
        if (targetFollow != null)
        {
            Vector3 modelPos = new Vector3(targetFollow.transform.position.x, /*targetFollow.transform.position.y - 1.48f*/0, targetFollow.transform.position.z);
            transform.position = modelPos;
        }
        Vector3 targetPostition = new Vector3(lookAt.transform.position.x,
                                       this.transform.position.y,
                                       lookAt.transform.position.z);
        //this.transform.LookAt(targetPostition);

        if (!isShooter)
            BaxterAnimation();
        
        //Vector3 lookPos = lookAt.transform.position - transform.position;
        //lookPos.y = 0;
        //Quaternion rotation = Quaternion.LookRotation(lookPos);
        //transform.rotation = Quaternion.Slerp(transform.rotation, rotation, Time.deltaTime * damping);
        //transform.rotation = Quaternion.Euler(0, 0, 0);
        //transform.rotation.
    }

    void BaxterAnimation()
    {
        Vector3 vDir = (transform.position - prevLoc) / Time.deltaTime;
        if (vDir.x > 0.5f)
        {
            //Debug.Log("Right");
            //animation.Play("Side Walk");
        }
        else if (vDir.x < -0.5f)
        {
            //Debug.Log("Left");
            //animation.Play("Side Walk");
        }

        if (vDir.z > 0.5f)
        {
            //Debug.Log("Forward");
            //animation.Play("Walk");
        }
        else if (vDir.z < -0.5f)
        {
            //Debug.Log("Back");
            //animation.Play("Walk");
        }

        anim.SetFloat("Velocity X", vDir.x);// * 0.1f);
        anim.SetFloat("Velocity Z", vDir.z);// * 0.1f);


        prevLoc = transform.position;
    }
}
